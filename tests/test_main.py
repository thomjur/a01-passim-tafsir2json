import unittest
import os
import json
import tempfile
import shutil
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main


class TestParseArguments(unittest.TestCase):
    def test_no_args(self):
        with patch('sys.argv', ['main.py']):
            sura, aya = main.parse_arguments()
            self.assertIsNone(sura)
            self.assertIsNone(aya)

    def test_only_sura_raises(self):
        with patch('sys.argv', ['main.py', '--sura', '2']):
            with self.assertRaises(SystemExit):
                main.parse_arguments()

    def test_only_aya_raises(self):
        with patch('sys.argv', ['main.py', '--aya', '255']):
            with self.assertRaises(SystemExit):
                main.parse_arguments()

    def test_both_args_long_flags(self):
        with patch('sys.argv', ['main.py', '--sura', '2', '--aya', '255']):
            sura, aya = main.parse_arguments()
            self.assertEqual(sura, 2)
            self.assertEqual(aya, 255)

    def test_both_args_short_flags(self):
        with patch('sys.argv', ['main.py', '-s', '3', '-a', '7']):
            sura, aya = main.parse_arguments()
            self.assertEqual(sura, 3)
            self.assertEqual(aya, 7)

class TestParseTafsirId(unittest.TestCase):
    def test_valid_filename(self):
        self.assertEqual(main.parse_tafsir_id("data/sc.123_45_67_89.txt"), "123")
        self.assertEqual(main.parse_tafsir_id("sc.1_2_3_4.txt"), "1")
        self.assertEqual(main.parse_tafsir_id("path/to/sc.999_1_1_1.txt"), "999")
    
    def test_invalid_filename_format(self):
        self.assertEqual(main.parse_tafsir_id("invalid.txt"), "")
        self.assertEqual(main.parse_tafsir_id("sc_123_45_67_89.txt"), "")
        self.assertEqual(main.parse_tafsir_id("sc.123_45_67.txt"), "")
        self.assertEqual(main.parse_tafsir_id("sc.123_45_67_89_90.txt"), "")
        self.assertEqual(main.parse_tafsir_id("sc.abc_45_67_89.txt"), "")


class TestAddMetadata(unittest.TestCase):
    def setUp(self):
        self.test_metadata = pd.DataFrame({
            'tafsir_id': [1, 28, 99, 99],
            'tafsir_title': ['Test Tafsir', 'Irshad al-aql', 'Multi-Author', 'Multi-Author'],
            'author_name': ['Author One', 'Abu al-Suud', 'First Author', 'Second Author'],
            'death_dce': [1500, 1574, 1600, 1650],
            'place_of_death': ['City A', 'Istanbul', 'City B', 'City C']
        })
    
    @patch('main.METADATA_EXISTS', True)
    @patch.object(main, 'df_metadata', new=None)
    def test_add_single_author_metadata(self):
        main.df_metadata = self.test_metadata
        
        input_dict = {}
        main.add_metadata(input_dict, "sc.1_2_3_4.txt")
        
        self.assertEqual(input_dict['tafsir_id'], "1")
        self.assertEqual(input_dict['tafsir_title'], 'Test Tafsir')
        self.assertEqual(input_dict['author_name'], 'Author One')
        self.assertEqual(input_dict['author_death_dce'], 1500)
        self.assertEqual(input_dict['author_place_of_death'], 'City A')
    
    @patch('main.METADATA_EXISTS', True)
    @patch.object(main, 'df_metadata', new=None)
    def test_add_multiple_authors_metadata(self):
        main.df_metadata = self.test_metadata
        
        input_dict = {}
        main.add_metadata(input_dict, "sc.99_2_3_4.txt")
        
        self.assertEqual(input_dict['tafsir_id'], "99")
        self.assertEqual(input_dict['tafsir_title'], 'Multi-Author')
        self.assertEqual(input_dict['author_name'], 'First Author')
        self.assertEqual(input_dict['author_name_2'], 'Second Author')
        self.assertEqual(input_dict['author_death_dce'], 1600)
        self.assertEqual(input_dict['author_death_dce_2'], 1650)
    
    @patch('main.METADATA_EXISTS', True)
    @patch('main.df_metadata')
    def test_metadata_not_found(self, mock_df):
        empty_df = pd.DataFrame()
        mock_df.loc.return_value.reset_index.return_value = empty_df
        
        input_dict = {}
        with patch('builtins.print') as mock_print:
            main.add_metadata(input_dict, "sc.999_2_3_4.txt")
            mock_print.assert_any_call("Could not retrieve Tafsir name")
    
    def test_invalid_tafsir_id(self):
        input_dict = {}
        with patch('builtins.print') as mock_print:
            main.add_metadata(input_dict, "invalid_filename.txt")
            mock_print.assert_called_with("Could not parse Tafsir id... aborting metadata retrieval.")


class TestCreateJson(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.temp_dir, "test_output.json")
        self.original_output_path = main.OUTPUT_FILE_PATH
        main.OUTPUT_FILE_PATH = self.output_file
    
    def tearDown(self):
        main.OUTPUT_FILE_PATH = self.original_output_path
        shutil.rmtree(self.temp_dir)
    
    @patch('main.METADATA_EXISTS', False)
    @patch('uuid.uuid4')
    def test_create_json_without_metadata(self, mock_uuid):
        mock_uuid.return_value = MagicMock(__str__=lambda x: "test-uuid-1234")
        
        test_content = "Test content for JSON creation"
        mock_file = MagicMock()
        mock_file.name = "test_file.txt"
        mock_file.read.return_value = test_content
        
        main.create_json(mock_file)
        
        with open(self.output_file, 'r') as f:
            result = json.loads(f.readline())
        
        self.assertEqual(result['id'], "tafsir.subchaptertest-uuid-1234")
        self.assertEqual(result['series'], "test-uuid-1234")
        self.assertEqual(result['text'], test_content)
    
    @patch('main.METADATA_EXISTS', True)
    @patch('main.add_metadata')
    @patch('uuid.uuid4')
    def test_create_json_with_metadata(self, mock_uuid, mock_add_metadata):
        mock_uuid.return_value = MagicMock(__str__=lambda x: "test-uuid-5678")
        
        def add_test_metadata(input_dict, filename):
            input_dict['tafsir_id'] = "28"
            input_dict['tafsir_title'] = "Test Tafsir"
            input_dict['author_name'] = "Test Author"
        
        mock_add_metadata.side_effect = add_test_metadata
        
        test_content = "Test content with metadata"
        mock_file = MagicMock()
        mock_file.name = "sc.28_1_1_1.txt"
        mock_file.read.return_value = test_content
        
        main.create_json(mock_file)
        
        with open(self.output_file, 'r') as f:
            result = json.loads(f.readline())
        
        self.assertEqual(result['id'], "tafsir.subchaptertest-uuid-5678")
        self.assertEqual(result['series'], "test-uuid-5678")
        self.assertEqual(result['text'], test_content)
        self.assertEqual(result['tafsir_id'], "28")
        self.assertEqual(result['tafsir_title'], "Test Tafsir")
        self.assertEqual(result['author_name'], "Test Author")


class TestMainFunction(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.temp_dir, "data")
        self.output_dir = os.path.join(self.temp_dir, "json")
        os.makedirs(self.data_dir)
        os.makedirs(self.output_dir)
        
        self.original_data_path = main.DATA_PATH
        self.original_output_path = main.OUTPUT_FILE_PATH
        main.DATA_PATH = self.data_dir + "/"
        main.OUTPUT_FILE_PATH = os.path.join(self.output_dir, "passim_input.json")
    
    def tearDown(self):
        main.DATA_PATH = self.original_data_path
        main.OUTPUT_FILE_PATH = self.original_output_path
        shutil.rmtree(self.temp_dir)
    
    @patch('main.METADATA_EXISTS', False)
    def test_main_processes_all_files(self):
        test_files = [
            ("sc.1_2_3_4.txt", "Content 1"),
            ("sc.28_5_10_15.txt", "Content 2"),
            ("sc.99_1_1_1.txt", "Content 3")
        ]
        
        for filename, content in test_files:
            with open(os.path.join(self.data_dir, filename), 'w') as f:
                f.write(content)
        
        main.main()
        
        with open(main.OUTPUT_FILE_PATH, 'r') as f:
            lines = f.readlines()
        
        self.assertEqual(len(lines), 3)
        
        for line in lines:
            data = json.loads(line)
            self.assertIn('id', data)
            self.assertIn('series', data)
            self.assertIn('text', data)
            self.assertTrue(data['text'] in ["Content 1", "Content 2", "Content 3"])


if __name__ == '__main__':
    unittest.main()
