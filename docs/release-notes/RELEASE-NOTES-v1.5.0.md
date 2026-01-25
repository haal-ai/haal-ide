# Release v1.5.0 - VSCode Extension & Enhanced User Experience

**Release Date:** 2025-09-26  
**Tag:** [v1.5.0](https://github.com/AmadeusITGroup/olaf/tree/v1.5.0)

## Overview

This release marks a significant milestone for new users discovering OLAF with the introduction of a comprehensive VSCode extension, automated installation capabilities, and enhanced documentation. The focus has been on improving user onboarding, streamlining installation, and providing practical examples for getting started.

## 🚀 New Features

- **VSCode Extension**: Complete VSCode extension with automated CI/CD pipeline for seamless OLAF installation and management across VSCode, Windsurf, Cursor, and Kiro IDEs
- **Automated Installation**: One-click installation system that automatically downloads and extracts OLAF components from GitHub releases
- **Getting Started Guide**: Comprehensive guide with real conversation examples and step-by-step usage patterns for new users
- **Presentation Creation**: New competencies for creating PowerPoint presentations and generating step-by-step tutorials
- **Learning Report System**: Mandatory learning report file saving with proper timestamp formatting

## 🛠️ Technical Improvements

- **CI/CD Pipeline**: Automated GitHub workflows for secure extension building, testing, and publishing
- **Bundle Distribution**: Automated release bundle creation and distribution system
- **Path Validation**: Enhanced validation for conversation records and presentation content
- **Python Migration**: Migrated PowerShell scripts to Python for better cross-platform compatibility
- **OSSF Scorecard**: Added security analysis with proper permissions configuration

## 📚 Documentation Enhancements

- **Installation Guide**: Updated installation documentation with VSCode extension instructions and improved structure
- **Research Branches**: Comprehensive overview of research branches with detailed implementation plans
- **Conversation Examples**: Real conversation records demonstrating OLAF capabilities and usage patterns
- **Version-Agnostic Content**: Cleaned up documentation to remove version-specific references for better maintainability

## 🔧 Framework Improvements

- **Directory Restructuring**: Moved project onboarding prompts to dedicated onboard directory for better organization
- **Competency Updates**: Enhanced competency index with new presentation and tutorial generation capabilities
- **Memory Map Updates**: Improved memory map structure for better LLM navigation
- **Template Enhancements**: Updated templates for presentation planning and tutorial creation

## 🧹 Maintenance & Cleanup

- **Code Complexity**: Removed reduce-code-complexity workflow (moved to research branch for restructuring)
- **CVE Verifier**: Removed CVE verifier functionality (moved to research-cve-verifier branch)
- **Gitignore Updates**: Enhanced .gitignore to handle VSCode extension artifacts and build outputs
- **Dependency Management**: Improved dependency handling and security configurations

## 💥 Contributors

- @pppaccau_amadeus (7 commits)
- @ppd (6 commits)  
- @Waldek Herka (3 commits)
- @pjmp020564 (2 commits)

## 📝 Upgrade Instructions

### For New Users
1. **Install VSCode Extension**: Search for "OLAF" in VSCode marketplace or install from VSIX
2. **Run Installation**: Use `OLAF: Install` command to automatically set up framework
3. **Explore Examples**: Review the getting started guide and conversation examples
4. **Try Competencies**: Start with simple competencies like `list competencies` or `research and report`

### For Existing Users
1. **Update Installation**: Use the new VSCode extension for easier management
2. **Review New Competencies**: Check out presentation creation and tutorial generation features
3. **Update Documentation**: Review updated installation and getting started guides
4. **Migrate Scripts**: Consider migrating any PowerShell scripts to Python equivalents

## 🔄 Breaking Changes

- **Installation Method**: While manual installation still works, VSCode extension is now the recommended approach
- **Script Dependencies**: Some PowerShell scripts have been migrated to Python (backward compatibility maintained)

## 📊 Statistics

- **18 commits** from v1.4.2 to HEAD
- **Major VSCode extension addition** with full CI/CD pipeline
- **Enhanced user onboarding** with practical examples and guides
- **Improved cross-platform compatibility** with Python migration

## 🎯 Target Audience Notes

This release is specifically designed for **new users discovering OLAF**:

- **Easy Installation**: VSCode extension provides one-click setup
- **Clear Documentation**: Step-by-step guides with real examples
- **Practical Examples**: Conversation records showing actual usage
- **Multiple IDE Support**: Works with VSCode, Windsurf
---

*Welcome to OLAF - Your AI Assistant Framework for Better LLM Collaboration*
