import streamlit as st
import difflib
import pandas as pd
import re

def main():
    st.title("Diff Checker")

    st.sidebar.header("Options")
    option = st.sidebar.selectbox("Choose an option", ["Compare Texts", "Merge Changes"])

    if option == "Compare Texts":
        compare_texts()
    elif option == "Merge Changes":
        merge_changes()

def compare_texts():
    st.header("Compare Texts")

    original_text = st.text_area("Original Text", height=200)
    changed_text = st.text_area("Changed Text", height=200)

    real_time_diff = st.checkbox("Real-time Diff", value=True)
    unified_diff = st.checkbox("Unified Diff", value=True)
    collapse_lines = st.checkbox("Collapse Lines", value=False)
    highlight_change = st.radio("Highlight Change", ["Word", "Character"], index=0)
    syntax_highlighting = st.selectbox("Choose Syntax", ["Plain Text", "Python", "JavaScript", "HTML", "CSS"])

    if real_time_diff or st.button("Compare"):
        original_lines = original_text.splitlines()
        changed_lines = changed_text.splitlines()

        if unified_diff:
            diff = difflib.unified_diff(original_lines, changed_lines, lineterm='')
        else:
            diff = difflib.ndiff(original_lines, changed_lines)

        result = '\n'.join(list(diff))

        if collapse_lines:
            result = collapse_unchanged_lines(result)

        if highlight_change == "Character":
            result = highlight_differences_by_character(result)
        else:
            result = highlight_differences_by_word(result)

        st.markdown(result, unsafe_allow_html=True)

def merge_changes():
    st.header("Merge Changes")

    original_text = st.text_area("Original Text", height=200)
    changed_text = st.text_area("Changed Text", height=200)

    if st.button("Merge"):
        original_lines = original_text.splitlines()
        changed_lines = changed_text.splitlines()

        diff = list(difflib.ndiff(original_lines, changed_lines))
        merged_text = '\n'.join([line[2:] for line in diff if not line.startswith('- ')])

        st.text_area("Merged Result", merged_text, height=200)

        if st.button("Merge Changes One by One"):
            merge_changes_one_by_one(diff)

def merge_changes_one_by_one(diff):
    st.header("Merge Changes One by One")

    merged_lines = []
    for line in diff:
        if line.startswith('- '):
            if st.button(f"Remove: {line[2:]}"):
                continue
        elif line.startswith('+ '):
            if st.button(f"Add: {line[2:]}"):
                merged_lines.append(line[2:])
        else:
            merged_lines.append(line[2:])

    merged_text = '\n'.join(merged_lines)
    st.text_area("Merged Result", merged_text, height=200)

def collapse_unchanged_lines(diff):
    lines = diff.split('\n')
    collapsed = []
    for line in lines:
        if line.startswith(' '):
            if len(collapsed) == 0 or not collapsed[-1].startswith('...'):
                collapsed.append('...')
        else:
            collapsed.append(line)
    return '\n'.join(collapsed)

def highlight_differences_by_character(diff):
    diff_lines = diff.split('\n')
    highlighted_diff = []
    for line in diff_lines:
        if line.startswith('+ '):
            highlighted_diff.append('<span style="background-color: #d4fcbc;">' + line + '</span>')
        elif line.startswith('- '):
            highlighted_diff.append('<span style="background-color: #fbb6c2;">' + line + '</span>')
        else:
            highlighted_diff.append(line)
    return '<br>'.join(highlighted_diff)

def highlight_differences_by_word(diff):
    diff_lines = diff.split('\n')
    highlighted_diff = []
    for line in diff_lines:
        if line.startswith('+ '):
            highlighted_diff.append('<span style="background-color: #d4fcbc;">' + highlight_words(line[2:], 'add') + '</span>')
        elif line.startswith('- '):
            highlighted_diff.append('<span style="background-color: #fbb6c2;">' + highlight_words(line[2:], 'remove') + '</span>')
        else:
            highlighted_diff.append(line)
    return '<br>'.join(highlighted_diff)

def highlight_words(text, change_type):
    words = text.split(' ')
    highlighted_words = []
    for word in words:
        if change_type == 'add':
            highlighted_words.append('<span style="background-color: #d4fcbc;">' + word + '</span>')
        elif change_type == 'remove':
            highlighted_words.append('<span style="background-color: #fbb6c2;">' + word + '</span>')
    return ' '.join(highlighted_words)

if __name__ == "__main__":
    main()