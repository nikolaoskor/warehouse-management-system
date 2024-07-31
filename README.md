# Warehouse Management System

## Description

This is an Warehouse Management System developed using Python and PostgreSQL. It allows users to perform CRUD operations on products, manage stock levels, and retrieve product statistics. The system includes features for managing orders, logging stock levels, and handling suppliers.

## Technologies Used

- **Python:** For implementing the backend logic and API endpoints.
- **FastAPI:** For creating RESTful APIs.
- **PostgreSQL:** For storing and managing inventory data.
- **Docker:** For containerization and easy deployment.

## Tools Used

- **Postman:** For testing API endpoints.
- **DBeaver:** For database management and visualization.
- **PyCharm:** For code editing and development.

## Features

1. **Product Management:**
   - **Create Product:** Add a new product with name, description, price, and stock level.
   - **Read Products:** Retrieve details of all products in the warehouse inventory.
   - **Update Product:** Modify details like price and stock level of existing products.
   - **Delete Product:** Remove a product from the warehouse inventory.
   - **Search Product:** Retrieve details of a product using its unique ID.

2. **Stock Management:**
   - Manage stock availability by increasing or decreasing quantities.

3. **Product Statistics:**
   - Retrieve statistics such as the number of products, average cost, total stock, etc.

## How to Run

Follow these steps to set up and run the application:

1. **Clone the Repository:**
   - Clone the repository to your local machine using the following command:
     ```bash
     git clone https://github.com/nikolaoskor/warehouse-management-system.git
     ```
   - Alternatively, download the project as a ZIP file from the repository and extract it to your desired location.

2. **Set Up the Database:**
   - Use Docker to run a PostgreSQL container:
     ```bash
     docker pull postgres
     docker run -d --name postgresCont -p 5432:5432 -e POSTGRES_PASSWORD=pass123 postgres
     ```
   - Connect to the database:
     ```bash
     docker exec -it postgresCont bash
     psql -h localhost -U postgres
     CREATE DATABASE postgres;
     \c postgres
     ```
   - Create the `products` table and insert initial data using the SQL scripts provided in the `db` folder. 

     To create the table, execute the SQL script `createTable.sql`:
     ```sql
     -- File: db/createTable.sql

     CREATE TABLE IF NOT EXISTS products (
         id SERIAL PRIMARY KEY,
         name VARCHAR(255) NOT NULL UNIQUE,
         description TEXT,
         price NUMERIC(10, 2) NOT NULL,
         stock INT NOT NULL
     );
     ```

     To insert initial data, execute the SQL script `insertValues.sql`:
     ```sql
     -- File: db/insertValues.sql

3. **Run the Application:**
   - Install the required Python packages:
     ```bash
     pip install fastapi psycopg2-binary uvicorn
     ```
   - Start the FastAPI server:
     ```bash
     uvicorn main:app --port 8080 --reload
     ```
   - The application will be accessible at `http://localhost:8080`.

## API Endpoints

### Product Management

- **Create Product**
  - **Endpoint:** `POST http://localhost:8080/product/new`
  - **Request Body:**
    ```json
    {
        "name": "apple 1kg",
        "description": "fruit",
        "price": 2.0,
        "stock": 120
    }
    ```
  - **Response:**
    ```json
    {
        "message": "Product: apple 1kg has been successfully created with price: 2.0€",
        "product": {
            "id": 1,
            "name": "apple 1kg",
            "description": "fruit",
            "price": 2.0,
            "stock": 120
        }
    }
    ```

- **Read Products**
  - **Endpoint:** `GET http://localhost:8080/product/all`
  - **Response:**
    ```json
    [
        {
            "id": 1,
            "name": "apple 1kg",
            "description": "fruit",
            "price": 2.0,
            "stock": 120
        },
        {
            "id": 2,
            "name": "banana 1kg",
            "description": "fruit",
            "price": 1.8,
            "stock": 150
        }
    ]
    ```

- **Update Product**
  - **Endpoint:** `PUT http://localhost:8080/product/update/{id}`
  - **Request Body:**
    ```json
    {
        "name": "apple 1kg",
        "description": "fruit",
        "price": 2.5,
        "stock": 110
    }
    ```
  - **Response:**
    ```json
    {
        "message": "Product (with id: 1) has been successfully updated",
        "product": {
            "id": 1,
            "name": "apple 1kg",
            "description": "fruit",
            "price": 2.5,
            "stock": 110
        }
    }
    ```

- **Delete Product**
  - **Endpoint:** `DELETE http://localhost:8080/product/delete/{id}`
  - **Response:**
    ```json
    {
        "message": "Product with ID: 1 has been successfully deleted."
    }
    ```

- **Search Product by ID**
  - **Endpoint:** `GET http://localhost:8080/product/{id}`
  - **Response:**
    ```json
    {
        "id": 1,
        "name": "apple 1kg",
        "description": "fruit",
        "price": 2.0,
        "stock": 120
    }
    ```

### Stock Management

- **Manage Stock**
  - **Endpoint:** `PUT http://localhost:8080/product/manage/{id}`
  - **Request Body:**
    ```json
    {
        "operation": "plus",
        "stock": 10
    }
    ```
  - **Response:**
    ```json
    {
        "message": "Product stock has been successfully increased.",
        "product": {
            "id": 1,
            "name": "apple 1kg",
            "description": "fruit",
            "price": 2.0,
            "stock": 130
        }
    }
    ```

### Product Statistics

- **Get Product Statistics**
  - **Endpoint:** `GET http://localhost:8080/product/products/statistics`
  - **Response:**
    ```json
    {
        "statistics": {
            "product sum": 21,
            "max price": 8.0,
            "min price": 0.5,
            "average price": 2.5,
            "total stock": 1980
        }
    }
    ```

## Testing Endpoints

1. Open [Postman](https://www.postman.com/).
2. Create a new request and set the method (GET, POST, PUT, DELETE) and URL as specified above.
3. Set the request body if required (for POST and PUT requests).
4. Send the request and verify the response.

## Notes

- Make sure to start the FastAPI server before testing the endpoints.
- You can use the SQL files in the `db` folder to set up the initial database schema and data.
