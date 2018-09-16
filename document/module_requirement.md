## Big Data ETL Autumation Requirement

1. User Management
  2. Login
  3. Logout
  4. Selfservice Account Creation

1. File Upload
  2. excel format only
  3. upload space control
  4. excel data extraction

1. Duplication Detection
  2. detection method
     ```
        if source.system.name not valid then
           return "Error"
        else
           if isValid(source.system.name) and source.table.name not in TableList then
              return "OK"
           else
              return "Error"
     ```
  3. detection result displaying
