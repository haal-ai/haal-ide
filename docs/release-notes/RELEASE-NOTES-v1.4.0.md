# Release v1.4.0 - Framework Restructuring & Documentation Enhancement

**Release Date:** 2025-09-11  
**Tag:** [v1.4.0](https://github.com/AmadeusITGroup/olaf/tree/v1.4.0)

## Overview

This release represents a major restructuring of the OLAF framework with comprehensive directory reorganization, enhanced documentation, and streamlined competency management. The focus has been on improving project maintainability, user onboarding, and framework clarity.

## 🏗️ Framework Restructuring

- **Directory Reorganization**: Renamed core directories from `ack`/`ads` to `core`/`data` for better clarity and branding alignment
- **Competency Consolidation**: Moved and reorganized competencies across roles for better logical grouping
- **Template Restructuring**: Reorganized all templates to match new directory structure
- **Tool Migration**: Updated all PowerShell tools and scripts to reflect new paths

## 📚 Documentation Enhancements

- **Branching Strategy**: Added comprehensive branching strategy documentation with workflow and protection rules
- **Installation Guide**: Created detailed installation guide and quick setup instructions  
- **Project Onboarding**: Enhanced project onboarding competency with structured orchestrator approach
- **Research Framework**: Added comprehensive GenAI solution assessment framework with structured questionnaire

## 🔧 Technical Improvements

- **Code Organization**: Moved examples and internal documentation to separate branches for cleaner main repository
- **Competency Cleanup**: Removed deprecated troubleshooting workflows and obsolete competencies
- **Path Normalization**: Fixed file references and path consistency across all components
- **Template Updates**: Updated all templates to use new directory structure and naming conventions

## 🧹 Maintenance & Cleanup

- **Deprecated Content Removal**: Removed experimental prompts, cloud-native architecture templates, and outdated competencies
- **Role Reorganization**: Moved competencies to more appropriate roles (e.g., research-and-report from business-analyst to researcher)
- **File Consolidation**: Consolidated related files and removed duplicates
- **Archive Management**: Moved historical content to appropriate archive locations

## 🛠️ New Tools & Components

- **Project Onboarding Tools**: Added Python-based analyzers for complexity, contributors, hotspots, and language distribution
- **Enhanced CVE Analysis**: Improved CVE verification workflow and tools
- **Research Protocols**: Added structured research and reporting frameworks

## 💥 Contributors

@pppaccau_amadeus (26 commits)

## 📝 Upgrade Instructions

1. **Update Directory References**: If you have custom scripts or configurations referencing the old `ack`/`ads` directories, update them to use `core`/`data`
2. **Review Competency Changes**: Check if any removed competencies were being used in your workflows
3. **Update Templates**: Any custom templates should be updated to match the new structure
4. **Path Updates**: Update any hardcoded paths in your local configurations

## 🔄 Breaking Changes

- **Directory Structure**: The `ack` and `ads` directories have been renamed to `core` and `data` respectively
- **Competency Removal**: Several deprecated competencies have been removed (troubleshooting workflows, cloud-native architecture prompts)
- **Template Locations**: All template paths have changed due to directory restructuring

## 📊 Statistics

- **26 commits** from v1.3.0 to HEAD
- **Major directory restructuring** affecting 200+ files
- **Enhanced documentation** with new installation and branching guides
- **Streamlined competency framework** with role-based organization
