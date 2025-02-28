import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401

import HealthCheckAnalyzeLargeInvestigations

LARGEST_INCIDENTS = [
    {
        'Size(MB)': 50,
        'AmountOfEntries': 100,
    },
    {
        'Size(MB)': 500,
        'AmountOfEntries': 100,
    },
    {
        'Size(MB)': 1,
        'AmountOfEntries': 1000,
    },
]


def test_format_dict_keys():
    given = LARGEST_INCIDENTS
    expected = [
        {'size': '50 MB', 'amountofentries': 100},
        {'size': '500 MB', 'amountofentries': 100},
        {'size': '1 MB', 'amountofentries': 1000},
    ]
    output = HealthCheckAnalyzeLargeInvestigations.format_dict_keys(given)

    assert output == expected


def test_main(mocker):
    # Set
    execute_command = mocker.patch.object(demisto, 'executeCommand', return_value=[{
        'Type': EntryType.NOTE,
        'Contents': {
            'data': LARGEST_INCIDENTS,
            'total': len(LARGEST_INCIDENTS),
        }
    }])
    # mocker.patch.object(demisto, 'executeCommand', return_value=LARGEST_INCIDENTS)
    args = {'Thresholds': {
        'numberofincidentswithmorethan500entries': 0,
        'numberofincidentsbiggerthan10mb': 0,
        'numberofincidentsbiggerthan1mb': 0,
    }}

    # Arrange
    result = HealthCheckAnalyzeLargeInvestigations.main(args)
    set_incident_fields = execute_command.call_args.args[1]

    # Assert
    assert len(result.outputs) == 3
    assert set_incident_fields['healthchecknumberofinvestigationsbiggerthan1mb'] == 3
    assert set_incident_fields['healthchecknumberofinvestigationsbiggerthan10mb'] == 2
    assert set_incident_fields['healthchecknumberofinvestigationswithmorethan500entries'] == 1
