import unittest
import argparse

# Unit tests:
from handleclient_noaccess_test import EUDATHandleClientNoaccessTestCase
from handleclient_readaccess_faked_test import EUDATHandleClientReadaccessFakedTestCase
from handleclient_readaccess_patched import EUDATHandleClientReadaccessPatchedTestCase
from handleclient_readaccess_faked_10320_test import EUDATHandleClientReadaccessFaked10320locTestCase
from clientcredentials_test import PIDClientCredentialsTestCase
from handleclient_search_noaccess_test import EUDATHandleClientSearchNoAccessTestCase

# Integration tests:
from handleclient_readaccess_test import EUDATHandleClientReadaccessTestCase
from handleclient_searchaccess_test import EUDATHandleClientSearchTestCase
from handleclient_writeaccess_test import EUDATHandleClientWriteaccessTestCase
from handleclient_writeaccess_10320_test import EUDATHandleClientWriteaccess10320locTestCase


if __name__ == '__main__':
    desc = 'Test script for b2handle library, including unit tests and integration '+\
           'tests. The integration tests need either read access to a handle server '+\
           'containing some specific test handle record (read), write access to a '+\
           ' handle server (write) or read access to a search servlet (search).'
    
    parser = argparse.ArgumentParser(description=desc)
    
    # Reading test types from args:
    parser.add_argument('testtype', metavar='testtype', nargs='*',
                   help='a test type to run (unit, read, write, and/or search)',
                   default=["unit"], action="store")
    param = parser.parse_args()
    print("Specified test types: "+str(param.testtype))

    write_access = False
    search_access = False
    no_access = False
    mocked_access = False
    read_access = False

    if 'unit' in param.testtype:
        no_access = True
        mocked_access = True
    if 'read' in param.testtype:
        read_access = True
    if 'write' in param.testtype:
        write_access = True
    if 'search' in param.testtype:
        search_access = True

    # Collection tests:
    verbosity = 5
    descriptions = 0

    print '\nCollecting tests:'
    tests_to_run = []
    numtests = 0
    if no_access:

        noaccess = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientNoaccessTestCase)
        tests_to_run.append(noaccess)
        n = noaccess.countTestCases()
        numtests += n
        print 'Number of tests for client (no access required):\t\t\t\t'+str(n)
        
        credentials = unittest.TestLoader().loadTestsFromTestCase(PIDClientCredentialsTestCase)
        tests_to_run.append(credentials)
        n = credentials.countTestCases()
        numtests += n
        print 'Number of tests for PIDClientCredentials:\t\t\t\t\t'+str(n)

        search_noaccess = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientSearchNoAccessTestCase)
        tests_to_run.append(search_noaccess)
        n = search_noaccess.countTestCases()
        numtests += n
        print 'Number of tests for searching (without server access):\t\t\t\t'+str(n)

    if mocked_access:

        mocked_read = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientReadaccessFakedTestCase)
        tests_to_run.append(mocked_read)
        n = mocked_read.countTestCases()
        numtests += n
        print 'Number of tests for client (faked read access):\t\t\t\t\t'+str(n)

        mocked_read_10320loc = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientReadaccessFaked10320locTestCase)
        tests_to_run.append(mocked_read_10320loc)
        n = mocked_read_10320loc.countTestCases()
        numtests += n
        print 'Number of tests for client\'s 10320/loc (faked read access):\t\t\t'+str(n)

        mocky = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientReadaccessPatchedTestCase)
        tests_to_run.append(mocky)
        n=mocky.countTestCases()
        numtests += no_access
        print 'Number of tests for MOCK:\t\t\t\t\t'+str(n)


    if read_access:

        read = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientReadaccessTestCase)
        tests_to_run.append(read)
        n = read.countTestCases()
        numtests += n
        print 'Number of integration tests for client (read access required):\t\t\t'+str(n)

    if write_access:

        write = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientWriteaccessTestCase)
        tests_to_run.append(write)
        n = write.countTestCases()
        numtests += n
        print 'Number of integration tests for client (write access required):\t\t\t'+str(n)
        
        write_10320loc = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientWriteaccess10320locTestCase)
        tests_to_run.append(write_10320loc)
        n = write_10320loc.countTestCases()
        numtests += n
        print 'Number of integration tests for 10320/loc (write access required):\t\t'+str(n)

    if search_access:

        search = unittest.TestLoader().loadTestsFromTestCase(EUDATHandleClientSearchTestCase)
        tests_to_run.append(search)
        n = search.countTestCases()
        numtests += n
        print 'Number of integration tests for searching (search servlet access required):\t'+str(n)

    # Run them
    print 'Run '+str(numtests)+' tests.'
    test_suites = unittest.TestSuite(tests_to_run)
    print '\nStarting tests:'
    unittest.TextTestRunner(descriptions=descriptions, verbosity=verbosity).run(test_suites)

    # Run with:
    # python -m coverage run main_test_script.py
    # python -m coverage report