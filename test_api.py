#!/usr/bin/env python3
"""
Test script for the AI-Based Question Paper Moderation System API
Tests all major endpoints and functionality
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:5000/api"

def print_test(test_name):
    """Print test header"""
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print('='*70)

def test_health_check():
    """Test health check endpoint"""
    print_test("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200, "Health check failed"
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_text_analysis():
    """Test text analysis endpoint"""
    print_test("Text Analysis")
    try:
        test_questions = [
            "Define the term algorithm and explain its importance in computer science.",
            "List the main components of a neural network.",
            "Analyze the time complexity of bubble sort algorithm.",
            "Evaluate the effectiveness of different sorting algorithms.",
            "Create a hypothesis about machine learning applications."
        ]
        
        data = {
            "questions": test_questions,
            "professor_name": "Test Professor",
            "subject": "Computer Science"
        }
        
        response = requests.post(f"{BASE_URL}/analyze", json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nPaper ID: {result['paper_id']}")
            print(f"Total Questions: {result['total_questions']}")
            print(f"\nBloom's Distribution:")
            for level, count in result['analysis']['blooms_distribution'].items():
                print(f"  {level}: {count}")
            print(f"\nDifficulty Distribution:")
            for level, count in result['analysis']['difficulty_distribution'].items():
                print(f"  {level}: {count}")
            print(f"\nSuggestions: {len(result['suggestions'])}")
            print("✓ PASSED")
            return result['paper_id']
        else:
            print(f"✗ FAILED: {response.text}")
            return None
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return None

def test_get_report(paper_id):
    """Test get report endpoint"""
    print_test(f"Get Report for Paper ID: {paper_id}")
    try:
        response = requests.get(f"{BASE_URL}/papers/{paper_id}/report")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nFilename: {result['filename']}")
            print(f"Subject: {result['subject']}")
            print(f"Professor: {result['professor_name']}")
            print(f"Overall Score: {result['overall_score']['score']}/100")
            print(f"Grade: {result['overall_score']['grade']}")
            print("✓ PASSED")
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_get_papers():
    """Test get all papers endpoint"""
    print_test("Get All Papers")
    try:
        response = requests.get(f"{BASE_URL}/papers")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nTotal Papers: {result['count']}")
            if result['count'] > 0:
                print("\nRecent Papers:")
                for paper in result['papers'][:3]:
                    print(f"  - ID: {paper['id']}, Subject: {paper['subject']}, Questions: {paper['total_questions']}")
            print("✓ PASSED")
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_statistics():
    """Test statistics endpoint"""
    print_test("System Statistics")
    try:
        response = requests.get(f"{BASE_URL}/statistics")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nTotal Papers: {result['total_papers']}")
            print(f"Total Questions: {result['total_questions']}")
            print(f"Average Quality Score: {result['average_quality_score']}")
            print("✓ PASSED")
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_file_upload():
    """Test file upload endpoint"""
    print_test("File Upload")
    try:
        # Use the existing draft_paper.txt
        if not os.path.exists('draft_paper.txt'):
            print("✗ SKIPPED: draft_paper.txt not found")
            return None
        
        with open('draft_paper.txt', 'rb') as f:
            files = {'file': ('draft_paper.txt', f, 'text/plain')}
            data = {
                'professor_name': 'Test Professor',
                'subject': 'General Science'
            }
            
            response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print(f"\nPaper ID: {result['paper_id']}")
                print(f"Filename: {result['filename']}")
                print(f"Total Questions: {result['total_questions']}")
                print("✓ PASSED")
                return result['paper_id']
            else:
                print(f"✗ FAILED: {response.text}")
                return None
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return None

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("AI-BASED QUESTION PAPER MODERATION SYSTEM - API TEST SUITE")
    print("="*70)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))
    time.sleep(0.5)
    
    # Test 2: Text Analysis
    paper_id = test_text_analysis()
    results.append(("Text Analysis", paper_id is not None))
    time.sleep(0.5)
    
    # Test 3: Get Report
    if paper_id:
        results.append(("Get Report", test_get_report(paper_id)))
        time.sleep(0.5)
    
    # Test 4: Get All Papers
    results.append(("Get All Papers", test_get_papers()))
    time.sleep(0.5)
    
    # Test 5: Statistics
    results.append(("Statistics", test_statistics()))
    time.sleep(0.5)
    
    # Test 6: File Upload
    upload_paper_id = test_file_upload()
    results.append(("File Upload", upload_paper_id is not None))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:.<50} {status}")
    
    print("="*70)
    print(f"Total: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n🎉 All tests passed! The system is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")

if __name__ == '__main__':
    print("\nWaiting for server to be ready...")
    time.sleep(2)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to server at http://localhost:5000")
        print("Please make sure the server is running with: python run.py")
