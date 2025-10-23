"""Batch processing with thread pool"""

from pathlib import Path
from typing import List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool, Slot
from loguru import logger

from bgremover.app.core.pipeline import get_pipeline
from bgremover.app.core.settings import OutputSettings, QualitySettings


class TaskStatus(Enum):
    """Task processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ProcessingTask:
    """Single image processing task"""
    id: int
    input_path: Path
    output_path: Path
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0
    error: Optional[str] = None


class WorkerSignals(QObject):
    """Signals for worker communication"""
    task_started = Signal(int)  # task_id
    task_progress = Signal(int, float)  # task_id, progress
    task_completed = Signal(int, Path)  # task_id, output_path
    task_failed = Signal(int, str)  # task_id, error
    batch_progress = Signal(int, int)  # completed, total
    batch_completed = Signal(int, int)  # successful, failed


class ProcessingWorker(QRunnable):
    """Worker for processing a single task"""
    
    def __init__(
        self,
        task: ProcessingTask,
        output_settings: OutputSettings,
        quality_settings: QualitySettings,
        signals: WorkerSignals
    ):
        super().__init__()
        self.task = task
        self.output_settings = output_settings
        self.quality_settings = quality_settings
        self.signals = signals
        self._cancelled = False
    
    def cancel(self):
        """Cancel this worker"""
        self._cancelled = True
    
    @Slot()
    def run(self):
        """Execute the processing task"""
        if self._cancelled:
            self.signals.task_failed.emit(self.task.id, "Cancelled")
            return
        
        try:
            # Emit start signal
            self.signals.task_started.emit(self.task.id)
            
            # Get pipeline
            pipeline = get_pipeline()
            
            # Process image
            success = pipeline.process_image(
                self.task.input_path,
                self.task.output_path,
                self.output_settings,
                self.quality_settings
            )
            
            if self._cancelled:
                self.signals.task_failed.emit(self.task.id, "Cancelled")
                return
            
            if success:
                self.signals.task_completed.emit(self.task.id, self.task.output_path)
            else:
                self.signals.task_failed.emit(self.task.id, "Processing failed")
        
        except Exception as e:
            logger.error(f"Worker error for task {self.task.id}: {e}")
            self.signals.task_failed.emit(self.task.id, str(e))


class BatchWorker(QObject):
    """Manages batch processing of multiple tasks"""
    
    # Signals
    task_started = Signal(int)
    task_progress = Signal(int, float)
    task_completed = Signal(int, Path)
    task_failed = Signal(int, str)
    batch_progress = Signal(int, int)  # completed, total
    batch_completed = Signal(int, int)  # successful, failed
    
    def __init__(self, max_workers: int = 4):
        super().__init__()
        
        self.max_workers = max_workers
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(max_workers)
        
        self.tasks: List[ProcessingTask] = []
        self.workers: List[ProcessingWorker] = []
        self.output_settings: Optional[OutputSettings] = None
        self.quality_settings: Optional[QualitySettings] = None
        
        self._cancelled = False
        self._paused = False
        self._completed_count = 0
        self._failed_count = 0
        
        # Setup signals
        self.signals = WorkerSignals()
        self.signals.task_started.connect(self._on_task_started)
        self.signals.task_completed.connect(self._on_task_completed)
        self.signals.task_failed.connect(self._on_task_failed)
    
    def add_tasks(
        self,
        input_paths: List[Path],
        output_dir: Path,
        output_settings: OutputSettings,
        quality_settings: QualitySettings,
        suffix: str = "_nobg"
    ) -> int:
        """
        Add tasks to the batch
        
        Args:
            input_paths: List of input image paths
            output_dir: Output directory
            output_settings: Output configuration
            quality_settings: Quality configuration
            suffix: Suffix to add to output filenames
        
        Returns:
            Number of tasks added
        """
        self.output_settings = output_settings
        self.quality_settings = quality_settings
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        task_id = len(self.tasks)
        added = 0
        
        for input_path in input_paths:
            # Create output filename
            output_filename = f"{input_path.stem}{suffix}.{output_settings.format}"
            output_path = output_dir / output_filename
            
            # Create task
            task = ProcessingTask(
                id=task_id,
                input_path=input_path,
                output_path=output_path
            )
            
            self.tasks.append(task)
            task_id += 1
            added += 1
        
        logger.info(f"Added {added} tasks to batch. Total: {len(self.tasks)}")
        return added
    
    def start(self) -> bool:
        """
        Start batch processing
        
        Returns:
            True if started successfully
        """
        if not self.tasks:
            logger.warning("No tasks to process")
            return False
        
        if self.output_settings is None or self.quality_settings is None:
            logger.error("Settings not configured")
            return False
        
        self._cancelled = False
        self._paused = False
        self._completed_count = 0
        self._failed_count = 0
        
        logger.info(f"Starting batch processing: {len(self.tasks)} tasks")
        
        # Create and start workers
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                worker = ProcessingWorker(
                    task,
                    self.output_settings,
                    self.quality_settings,
                    self.signals
                )
                
                self.workers.append(worker)
                self.thread_pool.start(worker)
        
        return True
    
    def pause(self):
        """Pause batch processing"""
        self._paused = True
        logger.info("Batch processing paused")
    
    def resume(self):
        """Resume batch processing"""
        self._paused = False
        logger.info("Batch processing resumed")
    
    def cancel(self):
        """Cancel batch processing"""
        self._cancelled = True
        
        # Cancel all workers
        for worker in self.workers:
            worker.cancel()
        
        # Wait for all to finish
        self.thread_pool.waitForDone()
        
        # Update task statuses
        for task in self.tasks:
            if task.status == TaskStatus.PROCESSING:
                task.status = TaskStatus.CANCELLED
        
        logger.info("Batch processing cancelled")
    
    def clear(self):
        """Clear all tasks"""
        self.cancel()
        self.tasks.clear()
        self.workers.clear()
        logger.info("Batch cleared")
    
    def get_status(self) -> dict:
        """
        Get current batch status
        
        Returns:
            Status dictionary with counts
        """
        pending = sum(1 for t in self.tasks if t.status == TaskStatus.PENDING)
        processing = sum(1 for t in self.tasks if t.status == TaskStatus.PROCESSING)
        completed = sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.tasks if t.status == TaskStatus.FAILED)
        cancelled = sum(1 for t in self.tasks if t.status == TaskStatus.CANCELLED)
        
        return {
            "total": len(self.tasks),
            "pending": pending,
            "processing": processing,
            "completed": completed,
            "failed": failed,
            "cancelled": cancelled,
            "is_running": processing > 0,
            "is_finished": (completed + failed + cancelled) == len(self.tasks)
        }
    
    @Slot(int)
    def _on_task_started(self, task_id: int):
        """Handle task started"""
        if task_id < len(self.tasks):
            self.tasks[task_id].status = TaskStatus.PROCESSING
            self.task_started.emit(task_id)
    
    @Slot(int, Path)
    def _on_task_completed(self, task_id: int, output_path: Path):
        """Handle task completed"""
        if task_id < len(self.tasks):
            self.tasks[task_id].status = TaskStatus.COMPLETED
            self.tasks[task_id].progress = 100.0
            
            self._completed_count += 1
            self.task_completed.emit(task_id, output_path)
            
            # Emit batch progress
            total_processed = self._completed_count + self._failed_count
            self.batch_progress.emit(total_processed, len(self.tasks))
            
            # Check if batch is complete
            if total_processed == len(self.tasks):
                self.batch_completed.emit(self._completed_count, self._failed_count)
                logger.success(
                    f"Batch completed: {self._completed_count} successful, "
                    f"{self._failed_count} failed"
                )
    
    @Slot(int, str)
    def _on_task_failed(self, task_id: int, error: str):
        """Handle task failed"""
        if task_id < len(self.tasks):
            self.tasks[task_id].status = TaskStatus.FAILED
            self.tasks[task_id].error = error
            
            self._failed_count += 1
            self.task_failed.emit(task_id, error)
            
            # Emit batch progress
            total_processed = self._completed_count + self._failed_count
            self.batch_progress.emit(total_processed, len(self.tasks))
            
            # Check if batch is complete
            if total_processed == len(self.tasks):
                self.batch_completed.emit(self._completed_count, self._failed_count)
                logger.success(
                    f"Batch completed: {self._completed_count} successful, "
                    f"{self._failed_count} failed"
                )
