# Viewing Jupyter Notebook Visualizations on GitHub

## The Problem
GitHub's notebook viewer doesn't execute code, so interactive Plotly visualizations appear as JSON text instead of charts.

## Solutions

### 1. **NBViewer (Recommended)**
- Go to [nbviewer.org](https://nbviewer.org/)
- Paste your GitHub notebook URL: 
  ```
  https://github.com/nish0753/phonepe_project/blob/main/Phonepe_Transaction.ipynb
  ```
- This will render all interactive charts properly

### 2. **Google Colab**
- Open [Google Colab](https://colab.research.google.com/)
- Use "File > Open notebook > GitHub" tab
- Enter your repository URL
- All visualizations will render interactively

### 3. **Local Environment**
- Clone the repository:
  ```bash
  git clone https://github.com/nish0753/phonepe_project.git
  cd phonepe_project
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Run Jupyter:
  ```bash
  jupyter notebook Phonepe_Transaction.ipynb
  ```

### 4. **Alternative: Static Images**
The notebook includes code to generate static PNG images of all charts. If the kaleido package works in your environment, uncomment the image export lines to generate static versions.

## Why This Happens
- GitHub shows notebooks as static HTML
- Interactive JavaScript elements (like Plotly) don't execute
- Only static content displays properly

## Best Practice
For GitHub portfolio projects, consider adding a "View Interactive Version" link in your README pointing to NBViewer or Colab.
