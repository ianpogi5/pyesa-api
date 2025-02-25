# PG Choir Pyesa

A choir companion API for Sunday Mass that serves mass songs. The application can be configured to read files from either Amazon S3 or a local filesystem.

## Features

- List available mass files
- Read mass song content
- Configurable file source (S3 or local filesystem)
- CORS enabled for cross-origin requests

## Prerequisites

- Python 3.7+
- AWS credentials (if using S3)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pg-choir-pyesa.git
   cd pg-choir-pyesa
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following configuration:

   Choose storage type: "S3" or "FS"

   ```bash
   FILES_FROM=FS
   ```

   Required for S3 storage

   ```bash
   S3_AWS_REGION=your-aws-region
   S3_BUCKET=your-bucket-name
   MASS_FILES=mass/
   ```

   Required for filesystem storage

   ```bash
   LOCAL_FILES_PATH=files/
   ```

4. Run the application:

   ```bash
   python main.py
   ```

   The API will be available at:

   - API: [http://localhost:8000](http://localhost:8000)
   - Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Project Structure

```bash
pyesa-api/
  ├── app.py # Main FastAPI application
  ├── lambda.py # AWS Lambda handler
  ├── main.py # Application entry point
  ├── requirements.txt # Project dependencies
  ├── files/ # Local storage directory for mass files
  └── .env # Environment configuration
```

## API Endpoints

### GET /

Welcome message endpoint

### GET /api/files

Lists all available JSON files

**Response:**

```json
{
  "files": ["2025-02-23 - 7th Sunday Ordinary Time(English).json"]
}
```

### GET /api/files/{filename}

Reads the content of a specific JSON file

**Response:**

```json
{
  "songs": [
    // Array of songs
  ]
}
```

## Error Handling

The API handles various error cases:

- 400: Invalid file type (non-JSON)
- 404: File not found
- 500: Server errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
