set_property(GLOBAL PROPERTY BAR VALUE)

set_property(DIRECTORY bar PROPERTY BAZ VALUE)

set_property(TARGET bar PROPERTY BAZ VALUE)

set_property(SOURCE bar PROPERTY BAZ VALUE)

set_property(INSTALL bar PROPERTY BAZ VALUE)

set_property(TEST bar PROPERTY BAZ VALUE)

set_property(CACHE bar PROPERTY BAZ VALUE)

set_property(CACHE foobar1 foobar2 foobar3 foobar4 foobar5 foobar6 foobar7 foobar8 foobar9 PROPERTY BAZ VALUE)

set_property(GLOBAL PROPERTY BAZ VALUE1 VALUE2 VALUE3 VALUE4 VALUE5 VALUE6 VALUE7 VALUE8 VALUE9 VALUE10 VALUE11)

set_property(GLOBAL APPEND PROPERTY BAZ VALUE)

set_property(GLOBAL APPEND_STRING PROPERTY BAZ VALUE)

set_property(GLOBAL PROPERTY LONG_PROPERTY_NAME_______________________________ VALUE)

set_property(GLOBAL PROPERTY LONG_PROPERTY_NAME_______________________________ VALUE1 VALUE2 VALUE3 VALUE4 VALUE5 VALUE6 VALUE7 VALUE8 VALUE9 VALUE10 VALUE11)

set_property(GLOBAL PROPERTY LONGER_PROPERTY_NAME_____________________________________________________ VALUE)

set_property(GLOBAL PROPERTY LONGER_PROPERTY_NAME_____________________________________________________ VALUE1 VALUE2 VALUE3 VALUE4 VALUE5 VALUE6 VALUE7 VALUE8 VALUE9 VALUE10 VALUE11)

set_property(DIRECTORY long_directory_name___________________________ PROPERTY BAR VALUE)

set_property(DIRECTORY longer_directory_name_________________________________________________ PROPERTY BAR VALUE)

set_property(DIRECTORY longer_directory_name_________________________________________________ PROPERTY BAR VALUE1 VALUE2 VALUE3 VALUE4 VALUE5 VALUE6 VALUE7 VALUE8 VALUE9 VALUE10 VALUE11)

set_property(DIRECTORY longer_directory_name_________________________________________________ PROPERTY LONG_PROPERTY_NAME_______________________________ VALUE)

set_property(DIRECTORY longer_directory_name_________________________________________________ PROPERTY LONG_PROPERTY_NAME_______________________________ VALUE1 VALUE2 VALUE3 VALUE4 VALUE5 VALUE6 VALUE7 VALUE8 VALUE9 VALUE10 VALUE11)

set_property(DIRECTORY longer_directory_name_________________________________________________ PROPERTY LONGER_PROPERTY_NAME_____________________________________________________ VALUE)

if(TRUE)
set_property(GLOBAL PROPERTY BAR VALUE)

set_property(GLOBAL PROPERTY LONG_PROPERTY_NAME_______________________________ VALUE1 VALUE2 VALUE3 VALUE4 VALUE5 VALUE6 VALUE7 VALUE8 VALUE9 VALUE10 VALUE11)
endif()

set_property(GLOBAL PROPERTY BAR_____________________________________________________________80 VALUE)

set_property(GLOBAL PROPERTY BAR______________________________________________________________81 VALUE)
