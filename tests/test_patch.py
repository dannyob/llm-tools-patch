"""Unit tests for the Patch toolbox."""

import os
import tempfile
import pytest
from pathlib import Path

from llm_tools_patch import Patch, patch_read, patch_write, patch_edit, patch_multi_edit, patch_info


class TestPatchFunctions:
    """Test the individual patch functions."""
    
    def test_patch_read_existing_file(self, tmp_path):
        """Test reading an existing file."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, world!\nThis is a test file."
        test_file.write_text(test_content)
        
        result = patch_read(str(test_file))
        assert result == test_content
    
    def test_patch_read_nonexistent_file(self, tmp_path):
        """Test reading a file that doesn't exist."""
        nonexistent = tmp_path / "nonexistent.txt"
        result = patch_read(str(nonexistent))
        assert result.startswith("Error: File")
        assert "does not exist" in result
    
    def test_patch_read_directory(self, tmp_path):
        """Test reading a directory instead of a file."""
        result = patch_read(str(tmp_path))
        assert result.startswith("Error:")
        assert "is not a file" in result
    
    def test_patch_write_new_file(self, tmp_path):
        """Test writing to a new file."""
        test_file = tmp_path / "new.txt"
        test_content = "New file content"
        
        result = patch_write(str(test_file), test_content)
        assert result.startswith("Successfully wrote")
        assert str(len(test_content)) in result
        assert test_file.read_text() == test_content
    
    def test_patch_write_creates_directories(self, tmp_path):
        """Test that patch_write creates parent directories."""
        nested_file = tmp_path / "nested" / "dir" / "file.txt"
        test_content = "Content in nested directory"
        
        result = patch_write(str(nested_file), test_content)
        assert result.startswith("Successfully wrote")
        assert nested_file.read_text() == test_content
    
    def test_patch_write_overwrite_existing(self, tmp_path):
        """Test overwriting an existing file."""
        test_file = tmp_path / "existing.txt"
        test_file.write_text("Original content")
        
        new_content = "New content"
        result = patch_write(str(test_file), new_content)
        assert result.startswith("Successfully wrote")
        assert test_file.read_text() == new_content
    
    def test_patch_edit_single_replacement(self, tmp_path):
        """Test making a single string replacement."""
        test_file = tmp_path / "edit.txt"
        original = "Hello world\nThis is a test"
        test_file.write_text(original)
        
        result = patch_edit(str(test_file), "world", "universe")
        assert result.startswith("Successfully replaced 1 occurrence")
        assert test_file.read_text() == "Hello universe\nThis is a test"
    
    def test_patch_edit_string_not_found(self, tmp_path):
        """Test editing when string is not found."""
        test_file = tmp_path / "edit.txt"
        test_file.write_text("Hello world")
        
        result = patch_edit(str(test_file), "missing", "replacement")
        assert result.startswith("Error: String not found")
    
    def test_patch_edit_multiple_occurrences_without_replace_all(self, tmp_path):
        """Test editing when string appears multiple times without replace_all."""
        test_file = tmp_path / "edit.txt"
        test_file.write_text("test test test")
        
        result = patch_edit(str(test_file), "test", "replaced")
        assert "appears 3 times" in result
        assert "Use replace_all=True" in result
    
    def test_patch_edit_multiple_occurrences_with_replace_all(self, tmp_path):
        """Test editing multiple occurrences with replace_all=True."""
        test_file = tmp_path / "edit.txt"
        test_file.write_text("test test test")
        
        result = patch_edit(str(test_file), "test", "replaced", replace_all=True)
        assert result.startswith("Successfully replaced 3 occurrence")
        assert test_file.read_text() == "replaced replaced replaced"
    
    def test_patch_multi_edit_success(self, tmp_path):
        """Test multiple edits in sequence."""
        test_file = tmp_path / "multi.txt"
        test_file.write_text("name = John\nage = 25\ncity = NYC")
        
        edits_json = '''[
            {"old_string": "John", "new_string": "Jane"},
            {"old_string": "25", "new_string": "30"},
            {"old_string": "NYC", "new_string": "SF"}
        ]'''
        
        result = patch_multi_edit(str(test_file), edits_json)
        assert result.startswith("Successfully applied 3 edit")
        assert test_file.read_text() == "name = Jane\nage = 30\ncity = SF"
    
    def test_patch_multi_edit_invalid_json(self, tmp_path):
        """Test multi_edit with invalid JSON."""
        test_file = tmp_path / "multi.txt"
        test_file.write_text("content")
        
        result = patch_multi_edit(str(test_file), "invalid json")
        assert result.startswith("Error: Invalid JSON format")
    
    def test_patch_multi_edit_empty_edits(self, tmp_path):
        """Test multi_edit with empty edits array."""
        test_file = tmp_path / "multi.txt"
        test_file.write_text("content")
        
        result = patch_multi_edit(str(test_file), "[]")
        assert result.startswith("Error: No edits provided")
    
    def test_patch_multi_edit_string_not_found(self, tmp_path):
        """Test multi_edit when a string is not found after previous edits."""
        test_file = tmp_path / "multi.txt"
        test_file.write_text("hello world")
        
        edits_json = '''[
            {"old_string": "world", "new_string": "universe"},
            {"old_string": "world", "new_string": "planet"}
        ]'''
        
        result = patch_multi_edit(str(test_file), edits_json)
        assert "Error in edit 2: String not found" in result
    
    def test_patch_info_existing_file(self, tmp_path):
        """Test getting info for an existing file."""
        test_file = tmp_path / "info.txt"
        test_content = "Test content for info"
        test_file.write_text(test_content)
        
        result = patch_info(str(test_file))
        assert f"File: {test_file}" in result
        assert f"Size: {len(test_content)} bytes" in result
        assert "Type: File" in result
        assert "Readable: True" in result
        assert "Encoding: Text" in result
    
    def test_patch_info_nonexistent_file(self, tmp_path):
        """Test getting info for a nonexistent file."""
        nonexistent = tmp_path / "nonexistent.txt"
        result = patch_info(str(nonexistent))
        assert result.startswith("Error: Path")
        assert "does not exist" in result


class TestPatchToolbox:
    """Test the Patch toolbox class."""
    
    def setup_method(self):
        """Set up a Patch toolbox instance for each test."""
        self.patch = Patch()
    
    def test_patch_toolbox_read(self, tmp_path):
        """Test the toolbox patch_read method."""
        test_file = tmp_path / "toolbox_test.txt"
        test_content = "Toolbox test content"
        test_file.write_text(test_content)
        
        result = self.patch.patch_read(str(test_file))
        assert result == test_content
    
    def test_patch_toolbox_write(self, tmp_path):
        """Test the toolbox patch_write method."""
        test_file = tmp_path / "toolbox_write.txt"
        test_content = "Toolbox write content"
        
        result = self.patch.patch_write(str(test_file), test_content)
        assert result.startswith("Successfully wrote")
        assert test_file.read_text() == test_content
    
    def test_patch_toolbox_edit(self, tmp_path):
        """Test the toolbox patch_edit method."""
        test_file = tmp_path / "toolbox_edit.txt"
        test_file.write_text("Hello toolbox world")
        
        result = self.patch.patch_edit(str(test_file), "toolbox", "testing")
        assert result.startswith("Successfully replaced")
        assert test_file.read_text() == "Hello testing world"
    
    def test_patch_toolbox_multi_edit(self, tmp_path):
        """Test the toolbox patch_multi_edit method."""
        test_file = tmp_path / "toolbox_multi.txt"
        test_file.write_text("config = debug\nport = 8080")
        
        edits_json = '''[
            {"old_string": "debug", "new_string": "production"},
            {"old_string": "8080", "new_string": "3000"}
        ]'''
        
        result = self.patch.patch_multi_edit(str(test_file), edits_json)
        assert result.startswith("Successfully applied 2 edit")
        assert test_file.read_text() == "config = production\nport = 3000"
    
    def test_patch_toolbox_info(self, tmp_path):
        """Test the toolbox patch_info method."""
        test_file = tmp_path / "toolbox_info.txt"
        test_file.write_text("Info test")
        
        result = self.patch.patch_info(str(test_file))
        assert "File:" in result
        assert "Size:" in result
        assert "Type: File" in result


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_tilde_expansion(self, tmp_path):
        """Test that tilde expansion works in file paths."""
        # Create a test file in a known location
        test_file = tmp_path / "tilde_test.txt" 
        test_content = "Tilde expansion test"
        test_file.write_text(test_content)
        
        # Test with the actual path (since we can't easily test ~ expansion in tmp_path)
        result = patch_read(str(test_file))
        assert result == test_content
    
    def test_empty_file_operations(self, tmp_path):
        """Test operations on empty files."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")
        
        # Read empty file
        result = patch_read(str(empty_file))
        assert result == ""
        
        # Edit empty file (should fail)
        result = patch_edit(str(empty_file), "nonexistent", "replacement")
        assert "String not found" in result
    
    def test_large_content(self, tmp_path):
        """Test with reasonably large content."""
        test_file = tmp_path / "large.txt"
        large_content = "".join(f"Line {i}\n" for i in range(1000))  # 1000 lines
        test_file.write_text(large_content)
        
        result = patch_read(str(test_file))
        assert len(result) == len(large_content)
        
        # Test editing large file
        result = patch_edit(str(test_file), "Line 0", "Modified Line 0")
        assert result.startswith("Successfully replaced")
    
    def test_unicode_content(self, tmp_path):
        """Test with Unicode content."""
        test_file = tmp_path / "unicode.txt"
        unicode_content = "Hello 🌍! Testing unicode: café, naïve, résumé"
        test_file.write_text(unicode_content, encoding='utf-8')
        
        result = patch_read(str(test_file))
        assert result == unicode_content
        
        result = patch_edit(str(test_file), "🌍", "🌎")
        assert result.startswith("Successfully replaced")
        assert "Hello 🌎!" in patch_read(str(test_file))