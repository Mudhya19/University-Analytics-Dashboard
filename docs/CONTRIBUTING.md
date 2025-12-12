# Contributing Guidelines

Panduan untuk berkontribusi pada University Analytics Dashboard project.

## Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test your changes: `pytest`
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature/your-feature`
6. Submit a Pull Request

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and modular

## Testing

Run tests before committing:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=src tests/
```
