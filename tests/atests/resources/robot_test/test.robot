*** Settings ***

Library  failurebase_sdk.robot.watcher

Library  keywords.py


Suite Setup    Initialize Failurebase    url=http://localhost:8000/api/events    no_proxy=127.0.0.1,localhost


*** Test Cases ***

Test Demo
    [Tags]    CIT    CRT
    Log To Console    Dumy test procedure
    Log To Console    ${1 / 0}    # fail!

Another failing test
    Log To Console    Let's fail it!
    Fail              msg=My custom message of fail!

Nested Failure
    show    Show....
    [Teardown]    Log To Console    Teardown :)

Own raises
    Raise sth

Fail in Setup
    [Setup]    Run Keywords    Sleep    1s    AND    Fail    msg=Setup failed
    No Operation
