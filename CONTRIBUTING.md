# Contributing to ProjectSpark

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VMaroon95/ProjectSpark.git
   cd ProjectSpark
   ```

2. **Backend setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

3. **Frontend:**
   Open `frontend/public/index.html` in a browser, or use any static file server:
   ```bash
   cd frontend
   npx serve -l 3000 .
   ```

4. **CLI:**
   ```bash
   python -m cli.runner --model meta-llama/Llama-3-8B --mode demo --output results.json
   ```

## Project Structure

- `cli/` — CLI benchmark tool (Python)
- `backend/` — FastAPI server
- `frontend/` — React dashboard (CDN-based, no build step)
- `data/` — Sample data files

## Guidelines

- Write clear, documented code
- Add type hints to Python functions
- Test your changes before submitting
- Keep commits focused and well-described

## Reporting Issues

Open an issue on GitHub with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, browser)

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
