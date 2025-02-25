# Pyesa API

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
   git clone https://github.com/ianpogi5/pyesa-api.git
   cd pyesa-api
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
    {
      "Id": 81,
      "author": "Bob Dufford",
      "Capo": 0,
      "content": "Intro: C--F-G-F-G-C-F-C (Short: C-F-G-G7)\n\n{c: Refrain}\n[C]Sing to the mountains, [F]sing to the s[G]ea.\n[C]Raise your [Am]voices, [Dm7]lift your [G]hearts.\n[G7/F]This is the [C/E]day the [Em]Lord has [A]made.\n[D]Let all the [G]earth re[C]jo[F]ic[C]e.\n\n{c: Verse 1}\n[F]I will give thanks to [C]you, my Lord.\n[G]You have [G7]answered my [C]plea.\n[E]You have [E7]saved my [Am]soul from [Am7/G]death.\n[Dm]You are my strength and [G]song.[G7]   ",
      "hash": "62936a6f23027920827f361b4bdce053",
      "key": 3,
      "KeyShift": 0,
      "name": "Sing to the Mountains",
      "subTitle": "",
      "type": 1,
      "ModifiedDateTime": "2025-02-20T01:05:07.855999Z",
      "Deleted": false,
      "SyncId": "",
      "timeSig": "3/4",
      "ZoomFactor": 1.0,
      "Duration": 0,
      "Duration2": 60,
      "_displayParams": "{}",
      "TempoInt": 0,
      "_tags": "[\"mass\",\"english\",\"opening\"]",
      "Url": "https://www.youtube.com/watch?v=0LWuT-fcMRM",
      "DeepSearch": "sing to the mountains\nbob dufford\ni will give thanks to you my lord\nsttm\n",
      "Copyright": "",
      "NotesText": "",
      "Zoom": 1.0,
      "SectionOrder": "",
      "SongNumber": 0,
      "HasChildren": 0,
      "ParentId": 0,
      "vName": null,
      "locked": 0,
      "LinkedAudio": null,
      "Chords": null,
      "midiOnLoad": null,
      "_folders": "[]"
    }
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
