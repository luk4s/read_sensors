# Changelog

## [1.1.0] - 2024-08-30
### Added
- new temperature sensor
### Changed
- gather sensors uuid based on their known serial number

## [1.0.0] - 2024-08-20
### Added
- Initial release of the project.
- Implemented `HomebridgeClient` with methods for authentication and fetching accessories.
- Added tests for `HomebridgeClient`.
- Created Docker setup with `Dockerfile` and `docker-entrypoint.sh` for running the script every minute.
- Configured `pytest` with fixtures and test cases.