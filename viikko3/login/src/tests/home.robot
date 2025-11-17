*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Starting Page

*** Test Cases ***
Click Login Link
    Click Link  Login
    Set Username  kalle
    Login Page Should Be Open

Click Register Link
    Click Link  Register new user
    Set Username  kalle
    Register Page Should Be Open

*** Keywords ***

Reset Application And Go To Starting Page
  Reset Application
  Go To Starting Page

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}