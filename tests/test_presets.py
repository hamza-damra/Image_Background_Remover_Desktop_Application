"""Test preset management"""

import pytest
from pathlib import Path

from bgremover.app.core.presets import PresetManager, Preset


@pytest.fixture
def preset_manager(tmp_path):
    """Create preset manager with temp directory"""
    manager = PresetManager()
    # Override presets directory for testing
    manager.presets_dir = tmp_path
    manager.presets_file = tmp_path / "custom_presets.json"
    return manager


def test_builtin_presets():
    """Test built-in presets"""
    manager = PresetManager()
    
    # Check that built-in presets exist
    assert "transparent" in manager.BUILTIN_PRESETS
    assert "marketplace" in manager.BUILTIN_PRESETS
    assert "white_bg" in manager.BUILTIN_PRESETS


def test_get_preset():
    """Test getting a preset"""
    manager = PresetManager()
    
    preset = manager.get_preset("transparent")
    assert preset is not None
    assert preset.name == "Transparent - Web"
    assert preset.background_type == "transparent"


def test_list_presets():
    """Test listing presets"""
    manager = PresetManager()
    
    presets = manager.list_presets()
    assert len(presets) > 0
    
    # Check structure
    for preset in presets:
        assert "id" in preset
        assert "name" in preset
        assert "description" in preset
        assert "type" in preset


def test_save_custom_preset(preset_manager):
    """Test saving custom preset"""
    custom_preset = Preset(
        name="My Custom Preset",
        description="Test preset",
        format="png",
        background_type="transparent"
    )
    
    success = preset_manager.save_preset("custom_test", custom_preset)
    assert success
    
    # Verify it was saved
    loaded = preset_manager.get_preset("custom_test")
    assert loaded is not None
    assert loaded.name == "My Custom Preset"


def test_delete_custom_preset(preset_manager):
    """Test deleting custom preset"""
    # Save a preset first
    custom_preset = Preset(
        name="To Delete",
        description="Will be deleted",
        format="png"
    )
    preset_manager.save_preset("delete_test", custom_preset)
    
    # Delete it
    success = preset_manager.delete_preset("delete_test")
    assert success
    
    # Verify it's gone
    assert preset_manager.get_preset("delete_test") is None


def test_cannot_delete_builtin(preset_manager):
    """Test that built-in presets cannot be deleted"""
    success = preset_manager.delete_preset("transparent")
    assert not success


def test_export_preset(preset_manager, tmp_path):
    """Test exporting preset"""
    export_path = tmp_path / "exported.json"
    
    success = preset_manager.export_preset("transparent", export_path)
    assert success
    assert export_path.exists()


def test_import_preset(preset_manager, tmp_path):
    """Test importing preset"""
    # First export a preset
    export_path = tmp_path / "to_import.json"
    preset_manager.export_preset("marketplace", export_path)
    
    # Import it with new ID
    success = preset_manager.import_preset(export_path, "imported_test")
    assert success
    
    # Verify it was imported
    loaded = preset_manager.get_preset("imported_test")
    assert loaded is not None
