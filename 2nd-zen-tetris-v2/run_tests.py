#!/usr/bin/env python3
"""
Test Runner for ZEN Tetris v2
全てのテストを実行し、バグ検証を行います
"""
import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_all_tests():
    """全テストを実行"""
    print("🧪 ZEN Tetris v2 - Comprehensive Bug Testing")
    print("=" * 50)
    
    # テストディスカバリー
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # 結果サマリー
    print("\n" + "=" * 50)
    print("🎯 Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, trace in result.failures:
            print(f"   - {test}")
            print(f"     {trace.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, trace in result.errors:
            print(f"   - {test}")
            print(f"     {trace.split('Error:')[-1].strip()}")
    
    # 全体評価
    if result.wasSuccessful():
        print("\n✅ All tests passed! No bugs detected.")
        print("🎋 ZEN Tetris v2 is ready for zen gaming experience.")
        return True
    else:
        print(f"\n❌ {len(result.failures + result.errors)} test(s) failed.")
        print("🔧 Please fix the issues before release.")
        return False

def run_specific_test(test_module):
    """特定のテストモジュールを実行"""
    print(f"🧪 Running {test_module} tests...")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f'tests.{test_module}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # 特定のテストモジュール実行
        test_module = sys.argv[1]
        success = run_specific_test(test_module)
    else:
        # 全テスト実行
        success = run_all_tests()
    
    sys.exit(0 if success else 1)