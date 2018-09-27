## Big Data ETL Autumation Requirement

1. User Management

        1. Login
        2. Logout
        3. Selfservice Account Creation

2. File Upload

        1.excel format only 
        2.upload space control
        3.excel data extraction

3. Duplication Detection

     detection method
     ```
        if source.system.name not valid then
           return "Error"
        else
           if isValid(source.system.name) and source.table.name not in TableList then
              return "OK"
           else
              return "Error"
     ```
4. detection result displaying
  
5. 增加已受理的标志字段
  
6. 增加更新已受理和已上线表的功能。
            
        上传excel，将该表中表名和来源表中系统匹配的数据表从已受理的表中删除;
        并将信息插入到已上线的表中。
  
7. 用户类型和权限
  
       用户类型：申请者、受理者、开发人员、管理员
       
8. 设计系统UI
