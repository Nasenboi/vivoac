<!---
    Write how an api request should be strucutred here!

-->


# API Request Structure

## HTTP Request Types

There are serveral HTTP request types that can be used to interact with the API. Those are: GET, POST, PUT, DELETE.
These methods are used to describe how the api endpoint interacts with the data on- or with the server.

- **GET**: Used to request / fetch / search for data from the server.
- **POST**: Used to create new data on the server. POST is also used to send other types of commands to the server!
- **PUT**: Used to update existing data on the server.
- **DELETE**: Used to delete data from the server. This also includes terminating sessions and logouts.

## Input Data

A HTTP reuest has multiple regions to send data from the user to the server. Each of them have their unique property and are being handled differently by the server.

- **Path**: Path parameters are variable strings that are inside of the URL of the HTTP request. The path is the part of the URL that comes after the domain. It is used to specify the resource that should be interacted with. In this particular project path parameters are rarely used.
- **Query**: Query paramters follow the URL and are used to send additional query information. So these parameters should only be used to filter the data that is being requested.
- **Header**: Header parameters are mostly hidden metadata. In this project header parameters are used to send the JWT authentication token and the current session id if required.
- **Body**: Body parameters are used to send the actual data that should be created or updated. The body is used to send the data that is being manipulated.

## API Endponts

Usually each route of this api does consist of the same, or similar endpoints. The most commun ones are described below:
- **GET route/{id}**: Get a single data record by its id.
- **GET route?<query>**: Searches for one or more data records that match the query.
- **POST route**: Creates a new data record.
- **PUT route/{id}**: Updates an existing data record by its id.
- **DELETE route/{id}**: Deletes an existing data record by its id.