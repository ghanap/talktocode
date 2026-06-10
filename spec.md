# Product Specification

## What are we building?
A "GitHub Automated Analysis Tool". It is a web application that takes a user's GitHub username, fetches all their public repositories, and uses AI to analyze and identify their most "technically complex" repository.

## Why are we building this?
Recruiters, hiring managers, and other developers often struggle to quickly identify the best or most challenging project in a candidate's portfolio. This tool automates the review process by analyzing repository metrics and contents, outputting a clear summary of why a specific repo is the most impressive.

## Core Requirements
- A clean, simple web interface where the user can enter a GitHub username.
- The system must fetch all public repositories for the given user via the GitHub API.
- The system must capture metadata (stars, forks, languages, contents, descriptions).
- The system must pass this data to a Large Language Model (LLM) using LangChain.
- The LLM must return the name, link, and a detailed analysis of the most complex repository.
- The system must handle invalid usernames gracefully.
