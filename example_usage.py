#!/usr/bin/env python3
"""
Example usage of the Caesar Data Collector Tool

This script demonstrates various ways to use the tool for collecting
data from the Caesar Twitter/X account.
"""

from caesar_data_collector import CaesarDataCollector
import json
import os

def example_basic_usage():
    """Basic usage example"""
    print("🔍 Example 1: Basic Usage")
    print("-" * 40)
    
    # Initialize collector with default settings
    collector = CaesarDataCollector()
    
    # Run full collection
    print("Running full data collection...")
    all_data = collector.run_full_collection()
    
    print(f"✅ Collection completed!")
    print(f"📁 Data saved to: {collector.output_dir}/")
    print(f"📊 Total sources: {all_data['collection_metadata']['total_sources']}")
    print(f"✅ Successful sources: {all_data['collection_metadata']['successful_sources']}")
    
    return all_data

def example_custom_output():
    """Example with custom output directory"""
    print("\n🔍 Example 2: Custom Output Directory")
    print("-" * 40)
    
    # Initialize with custom output directory
    custom_collector = CaesarDataCollector(output_dir="my_custom_caesar_data")
    
    # Run collection
    print("Running collection with custom output...")
    data = custom_collector.run_full_collection()
    
    print(f"✅ Custom collection completed!")
    print(f"📁 Data saved to: {custom_collector.output_dir}/")
    
    return data

def example_individual_components():
    """Example of running individual collection components"""
    print("\n🔍 Example 3: Individual Components")
    print("-" * 40)
    
    collector = CaesarDataCollector(output_dir="component_example")
    
    # Collect web data only
    print("Collecting web data...")
    web_data = collector.collect_web_data()
    print(f"Web data status: {web_data['status']}")
    
    # Collect archive data only
    print("Collecting archive data...")
    archive_data = collector.collect_archive_data()
    print(f"Archive data status: {archive_data['status']}")
    
    # Collect known data only
    print("Collecting known data...")
    known_data = collector.collect_known_data()
    print(f"Known data status: {known_data['status']}")
    
    # Create summary
    print("Creating summary...")
    summary = collector.create_data_summary()
    
    # Save individual components
    collector.save_data(web_data, 'web_only.json')
    collector.save_data(archive_data, 'archive_only.json')
    collector.save_data(known_data, 'known_only.json')
    collector.save_data(summary, 'summary_only.json')
    
    print(f"✅ Individual components saved to: {collector.output_dir}/")
    
    return {
        'web': web_data,
        'archive': archive_data,
        'known': known_data,
        'summary': summary
    }

def example_data_analysis():
    """Example of analyzing collected data"""
    print("\n🔍 Example 4: Data Analysis")
    print("-" * 40)
    
    # Load collected data
    try:
        with open('caesar_data/caesar_summary.json', 'r') as f:
            summary = json.load(f)
        
        print("📊 Data Analysis Results:")
        print(f"  • Account: @{summary['caesar_account']['username']}")
        print(f"  • Display Name: {summary['caesar_account']['display_name']}")
        print(f"  • Website: {summary['caesar_account']['website']}")
        
        print("\n🔑 Key Findings:")
        for key, value in summary['key_findings'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print("\n📈 Data Sources:")
        for source, description in summary['data_sources'].items():
            print(f"  • {source.replace('_', ' ').title()}: {description}")
            
    except FileNotFoundError:
        print("❌ No data found. Run collection first.")
        return None

def example_error_handling():
    """Example of error handling and retry logic"""
    print("\n🔍 Example 5: Error Handling")
    print("-" * 40)
    
    collector = CaesarDataCollector(output_dir="error_example")
    
    try:
        # Attempt collection with error handling
        print("Attempting data collection with error handling...")
        
        # Try web collection first
        try:
            web_data = collector.collect_web_data()
            if web_data['status'] == 'completed':
                print("✅ Web data collection successful")
            else:
                print(f"⚠️ Web data collection: {web_data['status']}")
        except Exception as e:
            print(f"❌ Web data collection failed: {str(e)}")
        
        # Try archive collection
        try:
            archive_data = collector.collect_archive_data()
            if archive_data['status'] == 'completed':
                print("✅ Archive data collection successful")
            else:
                print(f"⚠️ Archive data collection: {archive_data['status']}")
        except Exception as e:
            print(f"❌ Archive data collection failed: {str(e)}")
        
        # Known data should always work
        try:
            known_data = collector.collect_known_data()
            print("✅ Known data collection successful")
        except Exception as e:
            print(f"❌ Known data collection failed: {str(e)}")
        
        print("✅ Error handling example completed!")
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

def main():
    """Main function to run all examples"""
    print("🚀 Caesar Data Collector - Usage Examples")
    print("=" * 60)
    
    # Check if we have the required files
    if not os.path.exists('caesar_data_collector.py'):
        print("❌ Error: caesar_data_collector.py not found!")
        print("Please ensure you're in the correct directory.")
        return
    
    try:
        # Run examples
        print("Starting examples...\n")
        
        # Example 1: Basic usage
        example_basic_usage()
        
        # Example 2: Custom output
        example_custom_output()
        
        # Example 3: Individual components
        example_individual_components()
        
        # Example 4: Data analysis
        example_data_analysis()
        
        # Example 5: Error handling
        example_error_handling()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("\n📁 Check the created directories for output files:")
        print("  • caesar_data/")
        print("  • my_custom_caesar_data/")
        print("  • component_example/")
        print("  • error_example/")
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Please install required packages: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print("Check the error logs for more details.")

if __name__ == "__main__":
    main() 