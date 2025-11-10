#!/bin/bash

# Compilation script for Quantitative Finance Technical Report
# This script combines all chapter files and compiles the complete LaTeX document

echo "======================================================================"
echo "Quantitative Finance Technical Report - Compilation Script"
echo "======================================================================"
echo ""

# Check if LaTeX is installed
if ! command -v pdflatex &> /dev/null; then
    echo "ERROR: pdflatex not found. Please install a LaTeX distribution:"
    echo "  - macOS: brew install --cask mactex"
    echo "  - Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "  - Windows: Install MiKTeX from miktex.org"
    exit 1
fi

echo "Step 1: Creating complete document..."

# Create combined file
OUTPUT_FILE="Quantitative_Finance_Technical_Report.tex"

# Start with main file (has preamble and Chapter 1)
cp technical_report.tex "$OUTPUT_FILE"

# Remove the \end{document} from the main file
sed -i.bak '$d' "$OUTPUT_FILE"

# Append Chapter 2 (skip first line which is just a comment)
echo "" >> "$OUTPUT_FILE"
echo "% =====================================================================" >> "$OUTPUT_FILE"
echo "% CHAPTER 2: Stochastic Processes and Mean Reversion" >> "$OUTPUT_FILE"
echo "% =====================================================================" >> "$OUTPUT_FILE"
tail -n +1 chapter2_stochastic_processes.tex >> "$OUTPUT_FILE"

# Append Chapter 3
echo "" >> "$OUTPUT_FILE"
echo "% =====================================================================" >> "$OUTPUT_FILE"
echo "% CHAPTER 3: Stochastic Calculus and Option Pricing" >> "$OUTPUT_FILE"
echo "% =====================================================================" >> "$OUTPUT_FILE"
tail -n +1 chapter3_stochastic_calculus.tex >> "$OUTPUT_FILE"

# Append Chapter 4
echo "" >> "$OUTPUT_FILE"
echo "% =====================================================================" >> "$OUTPUT_FILE"
echo "% CHAPTER 4: Machine Learning for Financial Time Series" >> "$OUTPUT_FILE"
echo "% =====================================================================" >> "$OUTPUT_FILE"
tail -n +1 chapter4_machine_learning.tex >> "$OUTPUT_FILE"

# Append Chapter 5 (includes conclusion and end document)
echo "" >> "$OUTPUT_FILE"
echo "% =====================================================================" >> "$OUTPUT_FILE"
echo "% CHAPTER 5: Portfolio Optimization and Risk Management" >> "$OUTPUT_FILE"
echo "% =====================================================================" >> "$OUTPUT_FILE"
tail -n +1 chapter5_portfolio.tex >> "$OUTPUT_FILE"

echo "✓ Combined document created: $OUTPUT_FILE"
echo ""

echo "Step 2: First LaTeX compilation..."
pdflatex -interaction=nonstopmode "$OUTPUT_FILE" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ First compilation successful"
else
    echo "✗ First compilation had warnings (this is normal)"
fi
echo ""

echo "Step 3: Second LaTeX compilation (for references)..."
pdflatex -interaction=nonstopmode "$OUTPUT_FILE" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Second compilation successful"
else
    echo "✗ Second compilation had warnings"
fi
echo ""

# Check if PDF was generated
PDF_FILE="${OUTPUT_FILE%.tex}.pdf"
if [ -f "$PDF_FILE" ]; then
    echo "======================================================================"
    echo "SUCCESS! PDF generated: $PDF_FILE"
    echo "======================================================================"
    echo ""
    
    # Get file size
    FILE_SIZE=$(du -h "$PDF_FILE" | cut -f1)
    echo "File size: $FILE_SIZE"
    
    # Get page count (if pdfinfo is available)
    if command -v pdfinfo &> /dev/null; then
        PAGE_COUNT=$(pdfinfo "$PDF_FILE" 2>/dev/null | grep Pages | awk '{print $2}')
        echo "Total pages: $PAGE_COUNT"
    fi
    
    echo ""
    echo "Cleaning up auxiliary files..."
    rm -f *.aux *.log *.out *.toc *.lof *.lot *.bak
    echo "✓ Cleanup complete"
    echo ""
    
    echo "To view the PDF:"
    echo "  macOS:  open '$PDF_FILE'"
    echo "  Linux:  xdg-open '$PDF_FILE'"
    echo "  Windows: start '$PDF_FILE'"
    echo ""
else
    echo "======================================================================"
    echo "ERROR: PDF was not generated. Check compilation log for errors."
    echo "======================================================================"
    echo ""
    echo "Try running manually:"
    echo "  pdflatex $OUTPUT_FILE"
    echo ""
    echo "Check the .log file for detailed error messages:"
    echo "  cat ${OUTPUT_FILE%.tex}.log"
    exit 1
fi

echo "Compilation complete!"
echo ""
