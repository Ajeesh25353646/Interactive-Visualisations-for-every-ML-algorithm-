# Contributing to ML Algorithms Visualized

Thanks for your interest in contributing! This project visualizes ML algorithms to help people understand them intuitively. Every contribution helps.

## Ways to Contribute

### Report a bug
Open an issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce (which page, which slider, etc.)

### Request a visualization
Open an issue with:
- Which algorithm you want visualized
- What interactions you'd want (sliders, toggles, etc.)
- Why it's hard to understand without a visual

### Add a visualization
1. Fork the repo
2. Create your app in `apps/Your Algorithm/app.py`
3. Add a wrapper in `pages/X_Your_Algorithm.py`
4. Add a card in `Home.py` (follow the existing card pattern)
5. Submit a pull request

### Fix a bug
1. Fork the repo
2. Fix the issue
3. Test locally with `streamlit run Home.py --server.port 8520`
4. Submit a pull request

## Development Setup

```bash
pip install -r requirements.txt
streamlit run Home.py --server.port 8520 --server.headless true
```

## Style Guidelines

- Dark theme: use CSS variables from the existing pages
- No emojis in visible page content
- Use `st.latex()` for standalone math equations
- Plotly for charts, `st.metric()` for stats
- Every visualization should include interview questions at the bottom

## Adding a New Visualization

Each visualization needs:
1. **App file**: `apps/Your Algorithm/app.py` — standalone Streamlit app
2. **Wrapper**: `pages/X_Your Algorithm.py` — injects dark theme CSS, then execs the app
3. **Card**: Add to `Home.py` in the appropriate category section
4. **Interview section**: 3-5 questions interviewers actually ask about this algorithm

## Pull Request Process

1. Keep PRs focused — one feature or fix per PR
2. Test locally before submitting
3. Make sure the dark theme renders correctly
4. Include screenshots if changing UI

## Questions?

Open a Discussion in the repo.
