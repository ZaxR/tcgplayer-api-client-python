Changelog
==========
Based on https://keepachangelog.com/en/1.0.0/


## [0.1.0] - 2021-04-14

### Added:
- **previous entry to this file based on GitHub information**
- **functionality to BearerAuth for managing token expiration**
- **docstrings for BearerAuth class and all class functions**
- **timer functionality to TCGPlayerClient to ensure adherence to API call limit**
- **pagination to TCGPlayerClient's responses**
- **docstrings for TCGPlayerClient class and all class functions**

### Changed:
- **handling of client function args to better differentiate between path and query parameters**
- **format of this file to follow Markdown specs & read better**

## [0.0.3] 2020-06-01

### Added:
- **rest of API endpoints to v1.37.0.json**

### Changed:
- **how API version stored in TCGPlayerClient**
- **dynamic method generation**

## [0.0.2] - 2020-05-31

### Fixed:
- **typo in MANIFEST.in preventing api_specs from getting included, preventing client use**

## [0.0.1] - 2020-05-31

### Added:
- **base auth and client classes**
- **auto-generation of client methods from json spec**
- **four endpoints from api v1.37.0**