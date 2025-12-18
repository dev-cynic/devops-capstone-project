# devops-capstone-project

Customer Accounts Microservice for e-commerce website

[![Build Status](https://github.com/dev-cynic/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/dev-cynic/devops-capstone-project/actions/workflows/ci-build.yaml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)](https://shields.io/)

This repository contains the code for the Customer Accounts Microservice project for [**IBM-CD0285EN-SkillsNetwork DevOps Capstone Project**](https://www.coursera.org/learn/devops-capstone-project?specialization=devops-and-software-engineering) which is part of the [**IBM DevOps and Software Engineering Professional Certificate**](https://www.coursera.org/professional-certificates/devops-and-software-engineering)

## Project Overview
This capstone project involves developing a fully functional Customer Accounts microservice with REST API endpoints for creating, reading, updating, deleting, and listing customer accounts. The project follows Agile methodologies, test-driven development (TDD), and implements CI/CD pipelines using GitHub Actions, Docker, and Kubernetes.

## Features
- RESTful API endpoints for customer account management
- Test-driven development with 95%+ code coverage
- Containerization with Docker
- Deployment to Kubernetes/OpenShift
- CI/CD pipelines with GitHub Actions and Tekton
- Security implementation with Flask-Talisman and CORS

## Development Environment
These labs are designed to be executed in the IBM Developer Skills Network Cloud IDE with OpenShift. Please use the links provided in the Coursera Capstone project to access the lab environment.

Once you are in the lab environment, you can initialize it with `bin/setup.sh` by sourcing it. (*Note: DO NOT run this program as a bash script. It sets environment variable and so must be sourced*):

```bash
source bin/setup.sh