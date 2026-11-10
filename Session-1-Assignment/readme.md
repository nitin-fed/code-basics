# Workout Plan Generator

This project has two parts:

- **server**: the backend. It builds the workout plan.
- **ui**: the web page you use in your browser.

The server must be running before you use the UI.

## What you need

- [uv](https://docs.astral.sh/uv/getting-started/installation/), a tool that installs Python and the project's packages for you
- A Groq API key

## Setup (one time)

1. Create a file named `.env` in the `server` folder with your key:

   ```
   GROQ_API_KEY=your-key-here
   ```

2. Install the packages for each part:

   ```bash
   cd server
   uv sync
   cd ../ui
   uv sync
   ```

## Run the server

Open a terminal window and run:

```bash
cd server
uv run uvicorn app:app --reload
```

Leave this window open. The server runs at http://127.0.0.1:8000.

## Run the UI

Open a second terminal window and run:

```bash
cd ui
uv run streamlit run app.py
```

Your browser opens the page automatically. If it does not, go to http://localhost:8501.

## Using the app

1. Choose your fitness goal, experience level, and training days per week.
2. Select the equipment you have.
3. Optionally, describe any injuries or limitations.
4. Click **Generate plan**.

To stop either part, go to its terminal window and press `Ctrl + C`.
