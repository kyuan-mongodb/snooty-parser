from pathlib import Path

from . import rstparser
from .diagnostics import ExpectedPathArg, InvalidURL
from .n import FileId
from .parser import JSONVisitor
from .types import ProjectConfig
from .util_test import check_ast_testing_string, parse_rst

ROOT_PATH = Path("test_data")
FILEID = FileId("test.rst")


def test_openapi_using_filepath() -> None:
    project_config = ProjectConfig(ROOT_PATH, "", default_domain="mongodb", source="./")
    parser = rstparser.Parser(project_config, JSONVisitor)

    # Test default parse using file path
    page, diagnostics = parse_rst(
        parser,
        FILEID,
        """
.. openapi:: /test_parser/openapi-admin-v3.yaml
""",
    )
    page.finish(diagnostics)
    assert diagnostics == []
    check_ast_testing_string(
        page.ast,
        """
<root fileid="test.rst"><directive domain="mongodb" name="openapi" source_type="local"><text>/test_parser/openapi-admin-v3.yaml</text>
<text>{"openapi": "3.0.1", "info": {"description": "", "version": "3.0", "title": "MongoDB Realm API"}, "servers": [{"url": "https://realm.mongodb.com/api/admin/v3.0", "description": "The root API resource and starting point for the Realm API."}], "paths": {"/groups/{groupId}/apps/{appId}/services/{serviceId}": {"get": {"tags": ["services"], "operationId": "adminGetService", "summary": "Retrieve a :ref:`service &lt;services&gt;`.", "description": "Test description here.\\n", "responses": {"200": {"description": "The service was successfully deleted.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Service"}}}}}}, "delete": {"tags": ["services"], "operationId": "adminDeleteService", "summary": "Delete a :ref:`service &lt;services&gt;`.", "responses": {"204": {"description": "The service was successfully deleted."}}}, "patch": {"tags": ["services"], "operationId": "adminUpdateService", "summary": "Update a :ref:`service &lt;services&gt;`.", "responses": {"200": {"description": "Successfully updated."}}}, "parameters": [{"$ref": "#/components/parameters/GroupId"}, {"$ref": "#/components/parameters/AppId"}, {"$ref": "#/components/parameters/ServiceId"}]}, "/groups/{groupId}/apps/{appId}/logs": {"get": {"tags": ["logs"], "operationId": "adminGetLogs", "summary": "Retrieve MongoDB Realm logs.", "parameters": [{"name": "co_id", "in": "query", "description": "Return only log messages associated with the given request ID.", "schema": {"type": "string"}, "required": false}, {"name": "errors_only", "in": "query", "description": "Whether to only return errors.", "schema": {"type": "boolean"}, "required": false}, {"name": "user_id", "in": "query", "schema": {"type": "string"}, "description": "Return only log messages associated with the given ``user_id``.", "required": false}, {"name": "start_date", "in": "query", "schema": {"type": "string"}, "description": "The date and time in ISO 8601 at which to begin returning results, exclusive.", "required": false}, {"name": "end_date", "in": "query", "schema": {"type": "string"}, "description": "The date and time in ISO 8601 at which to cease returning results, inclusive.", "required": false}, {"name": "skip", "in": "query", "schema": {"type": "integer"}, "description": "The offset number of matching log entries to skip before including them in the response.", "required": false, "default": 0}, {"name": "limit", "in": "query", "schema": {"type": "integer", "minimum": 1, "maximum": 100}, "default": 100, "description": "The maximum number of log entries to include in the response. If the\\nquery matches more than this many logs, it returns documents in\\nascending order by date until the limit is reached.\\n", "required": false}], "responses": {"200": {"description": "Successfully retrieved.", "content": {"application/json": {"schema": {"type": "object", "properties": {"logs": {"type": "array", "items": {"type": "object", "properties": {"_id": {"type": "string"}, "co_id": {"type": "string"}, "domain_id": {"type": "string"}, "app_id": {"$ref": "#/components/parameters/AppId"}, "group_id": {"$ref": "#/components/parameters/GroupId"}, "request_url": {"type": "string"}, "request_method": {"type": "string"}, "started": {"type": "string"}, "completed": {"type": "string"}, "error": {"type": "string"}, "error_code": {"type": "string"}, "status": {"type": "integer"}}}}, "nextEndDate": {"type": "string", "required": false, "description": "The end date and time of the next page of log entries in ISO 8601 format. MongoDB Realm paginates the result sets of queries that match more than 100 log entries and includes this field in paginated responses. To get the next page of up to 100 entries, pass this value as the ``end_date`` parameter in a subsequent request."}, "nextSkip": {"type": "integer", "required": false, "description": "The offset into the next page of log entries in ISO 8601 format. MongoDB Realm paginates the result sets of queries that match more than 100 log entries and includes this field in paginated responses where the first entry on the next page has the same timestamp as the last entry on this page. To get the next page of up to 100 entries, pass this value, if it is present, as the ``skip`` parameter in a subsequent request."}}}}}}}}, "parameters": [{"$ref": "#/components/parameters/GroupId"}, {"$ref": "#/components/parameters/AppId"}]}, "/groups/{groupId}/apps/{appId}/api_keys": {"get": {"tags": ["apikeys"], "operationId": "adminListApiKeys", "summary": "List :doc:`API keys &lt;/authentication/api-key&gt;` associated with a Realm app.", "responses": {"200": {"description": "The API keys were successfully listed.", "content": {"application/json": {"schema": {"items": {"properties": {"_id": {"type": "string"}, "name": {"type": "string"}, "disabled": {"type": "boolean"}}}}}}}}}, "post": {"tags": ["apikeys"], "operationId": "adminCreateApiKey", "summary": "Create a new :doc:`API key &lt;/authentication/api-key&gt;`.", "requestBody": {"description": "The API key to create.", "required": true, "content": {"application/json": {"schema": {"properties": {"name": {"type": "string"}}, "required": ["name"]}}}}, "responses": {"201": {"description": "The API key was successfully created.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ApiKey"}}}}}}, "parameters": [{"$ref": "#/components/parameters/GroupId"}, {"$ref": "#/components/parameters/AppId"}]}, "/groups/{groupId}/apps/{appId}/measurements/": {"get": {"tags": ["billing"], "operationId": "adminAppMeasurements", "summary": "List the request, compute, sync, data transfer, and memory usage of a specific app in a given period for :doc:`billing &lt;/billing&gt;` purposes.", "parameters": [{"$ref": "#/components/parameters/GroupId"}, {"$ref": "#/components/parameters/AppId"}, {"name": "start", "in": "query", "description": "The ISO 8601 date and time of the start of the query period. Default is 00:00:00 UTC on the first day of the current month.", "schema": {"type": "string"}, "required": false}, {"name": "end", "in": "query", "description": "The ISO 8601 date and time of the end of the query period. Default is 23:59:59 UTC on the the last day of the current month.", "schema": {"type": "string"}, "required": false}, {"name": "granularity", "in": "query", "description": "Specifies the granularity of the query period, either P31D (31 day) or PT1H (1 hour). Default is P31D.", "schema": {"type": "string", "enum": ["P31D", "PT1H"]}, "required": false}], "responses": {"200": {"description": "The measurements were successfully returned.", "content": {"application/json": {"schema": {"properties": {"start": {"type": "string", "description": "The RFC 3339 date and time of the start of the query period, which can be specified with the ``start`` query parameter."}, "end": {"type": "string", "description": "The RFC 3339 date and time of the end of the query period, which can be specified with the ``end`` query parameter."}, "granularity": {"type": "string", "description": "The granularity, which can be specified with the ``granularity`` query parameter."}, "group_id": {"type": "string", "description": "The |atlas| :atlas:`Group ID &lt;/tutorial/manage-projects/&gt;`."}, "appId": {"type": "string", "description": "The Realm app ID specified by the ``appId`` path parameter."}, "appName": {"type": "string", "description": "The name of the Realm app specified by the ``appId`` path parameter."}, "measurements": {"type": "array", "description": "The array of measurements.\\n", "items": {"properties": {"name": {"type": "string", "enum": ["request_count", "compute_time", "data_out", "sync_time", "mem_usage"], "description": "The usage metric represented by each data point. See :doc:`billing &lt;/billing&gt;`. \\n"}, "units": {"type": "string", "enum": ["&lt;empty string&gt;", "HOURS", "GIGABYTES", "GIGABYTE_SECONDS"], "description": "The unit of the ``value`` of each data point.\\n"}, "data_points": {"type": "array", "description": "The array of data points for this measurement. A finer ``granularity`` results in more data points.\\n", "items": {"properties": {"timestamp": {"type": "string", "description": "The ISO 8601 date and time of the data point.\\n"}, "value": {"type": "number", "description": "The value at the time in the ``unit`` of the measurement.\\n"}}}}}}}}}}}}, "400": {"$ref": "#/components/responses/ClientErrorResponse"}}}}}, "components": {"parameters": {"GroupId": {"name": "groupId", "description": "An |atlas| :atlas:`Project/Group ID &lt;/tutorial/manage-projects/&gt;`.", "in": "path", "required": true, "schema": {"type": "string"}}, "AppId": {"name": "appId", "description": "The ObjectID of your application.\\n:ref:`realm-api-project-and-application-ids` demonstrates how\\nto find this value.\\n", "in": "path", "required": true, "schema": {"type": "string"}}, "ServiceId": {"name": "serviceId", "description": "Service ID", "in": "path", "required": true, "schema": {"type": "string"}}}, "schemas": {"ApiKey": {"properties": {"_id": {"type": "string"}, "key": {"type": "string"}, "name": {"type": "string"}, "disabled": {"type": "string"}}}, "Application": {"type": "object", "properties": {"_id": {"type": "string", "description": "The application's unique internal ID."}, "client_app_id": {"type": "string", "description": "The application's public App ID."}, "name": {"type": "string", "description": "The name of the application."}, "location": {"type": "string", "description": "The application's deployment region."}, "deployment_model": {"type": "string", "description": "The application's deployment model."}, "domain_id": {"type": "string"}, "group_id": {"$ref": "#/components/parameters/GroupId"}}}, "Service": {"properties": {"_id": {"type": "string"}, "name": {"type": "string"}, "type": {"type": "string"}, "version": {"type": "integer"}}}, "MetadataAttribute": {"type": "object", "properties": {"name": {"type": "string", "description": "The :doc:`metadata attribute &lt;/hosting/file-metadata-attributes&gt;` name."}, "value": {"type": "string", "description": "The :doc:`metadata attribute &lt;/hosting/file-metadata-attributes&gt;` value."}}}}, "securitySchemes": {"tokenAuth": {"type": "http", "scheme": "bearer", "description": "The authorization token provided in the ``access_token`` field of\\nthe :ref:`post-/auth/providers/{provider}/login` and\\n:ref:`post-/auth/session` API endpoints.\\n"}}, "responses": {"ClientErrorResponse": {"description": "There is an error in the request.", "content": {"application/json": {"schema": {"properties": {"error": {"type": "string", "description": "A message describing the error.\\n"}}}}}}}}, "tags": [{"name": "apikeys", "description": "API Key APIs"}, {"name": "billing", "description": "Billing APIs"}, {"name": "logs", "description": "Logging APIs"}, {"name": "services", "description": "Services APIs"}], "security": [{"tokenAuth": []}]}</text></directive></root>
        """,
    )


def test_openapi_using_url() -> None:
    project_config = ProjectConfig(ROOT_PATH, "", default_domain="mongodb", source="./")
    parser = rstparser.Parser(project_config, JSONVisitor)

    # Successful
    page, diagnostics = parse_rst(
        parser,
        FILEID,
        """
.. openapi:: https://raw.githubusercontent.com/mongodb/snooty-parser/master/test_data/test_parser/openapi-admin-v3.yaml
""",
    )
    page.finish(diagnostics)
    assert diagnostics == []
    check_ast_testing_string(
        page.ast,
        """
<root fileid="test.rst"><directive domain="mongodb" name="openapi" source_type="url"><reference refuri="https://raw.githubusercontent.com/mongodb/snooty-parser/master/test_data/test_parser/openapi-admin-v3.yaml"><text>https://raw.githubusercontent.com/mongodb/snooty-parser/master/test_data/test_parser/openapi-admin-v3.yaml</text></reference>
<text>{"openapi": "3.0.1", "info": {"description": "", "version": "3.0", "title": "MongoDB Realm API"}, "servers": [{"url": "https://realm.mongodb.com/api/admin/v3.0", "description": "The root API resource and starting point for the Realm API."}], "paths": {"/groups/{groupId}/apps/{appId}/services/{serviceId}": {"get": {"tags": ["services"], "operationId": "adminGetService", "summary": "Retrieve a :ref:`service &lt;services&gt;`.", "description": "Test description here.\\n", "responses": {"200": {"description": "The service was successfully deleted.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Service"}}}}}}, "delete": {"tags": ["services"], "operationId": "adminDeleteService", "summary": "Delete a :ref:`service &lt;services&gt;`.", "responses": {"204": {"description": "The service was successfully deleted."}}}, "patch": {"tags": ["services"], "operationId": "adminUpdateService", "summary": "Update a :ref:`service &lt;services&gt;`.", "responses": {"200": {"description": "Successfully updated."}}}, "parameters": [{"$ref": "#/components/parameters/GroupId"}, {"$ref": "#/components/parameters/AppId"}, {"$ref": "#/components/parameters/ServiceId"}]}, "/groups/{groupId}/apps/{appId}/logs": {"get": {"tags": ["logs"], "operationId": "adminGetLogs", "summary": "Retrieve MongoDB Realm logs.", "parameters": [{"name": "co_id", "in": "query", "description": "Return only log messages associated with the given request ID.", "schema": {"type": "string"}, "required": false}, {"name": "errors_only", "in": "query", "description": "Whether to only return errors.", "schema": {"type": "boolean"}, "required": false}, {"name": "user_id", "in": "query", "schema": {"type": "string"}, "description": "Return only log messages associated with the given ``user_id``.", "required": false}, {"name": "start_date", "in": "query", "schema": {"type": "string"}, "description": "The date and time in ISO 8601 at which to begin returning results, exclusive.", "required": false}, {"name": "end_date", "in": "query", "schema": {"type": "string"}, "description": "The date and time in ISO 8601 at which to cease returning results, inclusive.", "required": false}, {"name": "skip", "in": "query", "schema": {"type": "integer"}, "description": "The offset number of matching log entries to skip before including them in the response.", "required": false, "default": 0}, {"name": "limit", "in": "query", "schema": {"type": "integer", "minimum": 1, "maximum": 100}, "default": 100, "description": "The maximum number of log entries to include in the response. If the\\nquery matches more than this many logs, it returns documents in\\nascending order by date until the limit is reached.\\n", "required": false}], "responses": {"200": {"description": "Successfully retrieved.", "content": {"application/json": {"schema": {"type": "object", "properties": {"logs": {"type": "array", "items": {"type": "object", "properties": {"_id": {"type": "string"}, "co_id": {"type": "string"}, "domain_id": {"type": "string"}, "app_id": {"$ref": "#/components/parameters/AppId"}, "group_id": {"$ref": "#/components/parameters/GroupId"}, "request_url": {"type": "string"}, "request_method": {"type": "string"}, "started": {"type": "string"}, "completed": {"type": "string"}, "error": {"type": "string"}, "error_code": {"type": "string"}, "status": {"type": "integer"}}}}, "nextEndDate": {"type": "string", "required": false, "description": "The end date and time of the next page of log entries in ISO 8601 format. MongoDB Realm paginates the result sets of queries that match more than 100 log entries and includes this field in paginated responses. To get the next page of up to 100 entries, pass this value as the ``end_date`` parameter in a subsequent request."}, "nextSkip": {"type": "integer", "required": false, "description": "The offset into the next page of log entries in ISO 8601 format. MongoDB Realm paginates the result sets of queries that match more than 100 log entries and includes this field in paginated responses where the first entry on the next page has the same timestamp as the last entry on this page. To get the next page of up to 100 entries, pass this value, if it is present, as the ``skip`` parameter in a subsequent request."}}}}}}}}, "parameters": [{"$ref": "#/components/parameters/GroupId"}, {"$ref": "#/components/parameters/AppId"}]}, "/groups/{groupId}/apps/{appId}/api_keys": {"get": {"tags": ["apikeys"], "operationId": "adminListApiKeys", "summary": "List :doc:`API keys &lt;/authentication/api-key&gt;` associated with a Realm app.", "responses": {"200": {"description": "The API keys were successfully listed.", "content": {"application/json": {"schema": {"items": {"properties": {"_id": {"type": "string"}, "name": {"type": "string"}, "disabled": {"type": "boolean"}}}}}}}}}, "post": {"tags": ["apikeys"], "operationId": "adminCreateApiKey", "summary": "Create a new :doc:`API key &lt;/authentication/api-key&gt;`.", "requestBody": {"description": "The API key to create.", "required": true, "content": {"application/json": {"schema": {"properties": {"name": {"type": "string"}}, "required": ["name"]}}}}, "responses": {"201": {"description": "The API key was successfully created.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ApiKey"}}}}}}, "parameters": [{"$ref": "#/components/parameters/GroupId"}, {"$ref": "#/components/parameters/AppId"}]}, "/groups/{groupId}/apps/{appId}/measurements/": {"get": {"tags": ["billing"], "operationId": "adminAppMeasurements", "summary": "List the request, compute, sync, data transfer, and memory usage of a specific app in a given period for :doc:`billing &lt;/billing&gt;` purposes.", "parameters": [{"$ref": "#/components/parameters/GroupId"}, {"$ref": "#/components/parameters/AppId"}, {"name": "start", "in": "query", "description": "The ISO 8601 date and time of the start of the query period. Default is 00:00:00 UTC on the first day of the current month.", "schema": {"type": "string"}, "required": false}, {"name": "end", "in": "query", "description": "The ISO 8601 date and time of the end of the query period. Default is 23:59:59 UTC on the the last day of the current month.", "schema": {"type": "string"}, "required": false}, {"name": "granularity", "in": "query", "description": "Specifies the granularity of the query period, either P31D (31 day) or PT1H (1 hour). Default is P31D.", "schema": {"type": "string", "enum": ["P31D", "PT1H"]}, "required": false}], "responses": {"200": {"description": "The measurements were successfully returned.", "content": {"application/json": {"schema": {"properties": {"start": {"type": "string", "description": "The RFC 3339 date and time of the start of the query period, which can be specified with the ``start`` query parameter."}, "end": {"type": "string", "description": "The RFC 3339 date and time of the end of the query period, which can be specified with the ``end`` query parameter."}, "granularity": {"type": "string", "description": "The granularity, which can be specified with the ``granularity`` query parameter."}, "group_id": {"type": "string", "description": "The |atlas| :atlas:`Group ID &lt;/tutorial/manage-projects/&gt;`."}, "appId": {"type": "string", "description": "The Realm app ID specified by the ``appId`` path parameter."}, "appName": {"type": "string", "description": "The name of the Realm app specified by the ``appId`` path parameter."}, "measurements": {"type": "array", "description": "The array of measurements.\\n", "items": {"properties": {"name": {"type": "string", "enum": ["request_count", "compute_time", "data_out", "sync_time", "mem_usage"], "description": "The usage metric represented by each data point. See :doc:`billing &lt;/billing&gt;`. \\n"}, "units": {"type": "string", "enum": ["&lt;empty string&gt;", "HOURS", "GIGABYTES", "GIGABYTE_SECONDS"], "description": "The unit of the ``value`` of each data point.\\n"}, "data_points": {"type": "array", "description": "The array of data points for this measurement. A finer ``granularity`` results in more data points.\\n", "items": {"properties": {"timestamp": {"type": "string", "description": "The ISO 8601 date and time of the data point.\\n"}, "value": {"type": "number", "description": "The value at the time in the ``unit`` of the measurement.\\n"}}}}}}}}}}}}, "400": {"$ref": "#/components/responses/ClientErrorResponse"}}}}}, "components": {"parameters": {"GroupId": {"name": "groupId", "description": "An |atlas| :atlas:`Project/Group ID &lt;/tutorial/manage-projects/&gt;`.", "in": "path", "required": true, "schema": {"type": "string"}}, "AppId": {"name": "appId", "description": "The ObjectID of your application.\\n:ref:`realm-api-project-and-application-ids` demonstrates how\\nto find this value.\\n", "in": "path", "required": true, "schema": {"type": "string"}}, "ServiceId": {"name": "serviceId", "description": "Service ID", "in": "path", "required": true, "schema": {"type": "string"}}}, "schemas": {"ApiKey": {"properties": {"_id": {"type": "string"}, "key": {"type": "string"}, "name": {"type": "string"}, "disabled": {"type": "string"}}}, "Application": {"type": "object", "properties": {"_id": {"type": "string", "description": "The application's unique internal ID."}, "client_app_id": {"type": "string", "description": "The application's public App ID."}, "name": {"type": "string", "description": "The name of the application."}, "location": {"type": "string", "description": "The application's deployment region."}, "deployment_model": {"type": "string", "description": "The application's deployment model."}, "domain_id": {"type": "string"}, "group_id": {"$ref": "#/components/parameters/GroupId"}}}, "Service": {"properties": {"_id": {"type": "string"}, "name": {"type": "string"}, "type": {"type": "string"}, "version": {"type": "integer"}}}, "MetadataAttribute": {"type": "object", "properties": {"name": {"type": "string", "description": "The :doc:`metadata attribute &lt;/hosting/file-metadata-attributes&gt;` name."}, "value": {"type": "string", "description": "The :doc:`metadata attribute &lt;/hosting/file-metadata-attributes&gt;` value."}}}}, "securitySchemes": {"tokenAuth": {"type": "http", "scheme": "bearer", "description": "The authorization token provided in the ``access_token`` field of\\nthe :ref:`post-/auth/providers/{provider}/login` and\\n:ref:`post-/auth/session` API endpoints.\\n"}}, "responses": {"ClientErrorResponse": {"description": "There is an error in the request.", "content": {"application/json": {"schema": {"properties": {"error": {"type": "string", "description": "A message describing the error.\\n"}}}}}}}}, "tags": [{"name": "apikeys", "description": "API Key APIs"}, {"name": "billing", "description": "Billing APIs"}, {"name": "logs", "description": "Logging APIs"}, {"name": "services", "description": "Services APIs"}], "security": [{"tokenAuth": []}]}</text></directive></root>
        """,
    )

    # Invalid URL
    page, diagnostics = parse_rst(
        parser,
        FILEID,
        """
.. openapi:: https://mongodb.com
""",
    )
    page.finish(diagnostics)
    assert len(diagnostics) == 1
    assert isinstance(diagnostics[0], InvalidURL)


def test_openapi_using_realm() -> None:
    project_config = ProjectConfig(ROOT_PATH, "", default_domain="mongodb", source="./")
    parser = rstparser.Parser(project_config, JSONVisitor)

    page, diagnostics = parse_rst(
        parser,
        FILEID,
        """
.. openapi:: cloud
   :uses-realm:
""",
    )
    page.finish(diagnostics)
    assert diagnostics == []
    check_ast_testing_string(
        page.ast,
        """
<root fileid="test.rst">
  <directive domain="mongodb" name="openapi" uses-realm="True" source_type="atlas">
    <text>cloud</text>
  </directive>
</root>
        """,
    )

    page, diagnostics = parse_rst(
        parser,
        FILEID,
        """
.. openapi:: https://mongodb.com
   :uses-realm:
""",
    )
    page.finish(diagnostics)
    assert len(diagnostics) == 1
    assert isinstance(diagnostics[0], ExpectedPathArg)
