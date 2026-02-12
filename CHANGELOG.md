# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added comprehensive benchmark tests for performance-critical code paths
- Added `__slots__` to all monadic classes for memory efficiency
- Added copy support (`__copy__` and `__deepcopy__`) for all monadic types
- Added error type inheritance hierarchy with `RustyMonadError` base class
- Added `ResultGenericError` for better error handling and type annotations
- Added English comments to README.md for international contributors
- Added benchmark results documentation in BENCHMARK_RESULTS.md

### Changed
- Improved `do_notation` error messages for better debugging experience
- Unified `Ok` and `Err` class structure to reduce code duplication
- Standardized empty line style across all source files
- Fixed `TypeVar` pollution by using private TypeVars
- Fixed `Err.__hash__` potential issues with mutable default behavior
- Fixed `Some.and_then` return type consistency
- Fixed `Nothing` singleton implementation
- Fixed comment language to maintain consistency (English)

### Fixed
- Corrected type annotations for `Some.and_then` method
- Resolved singleton pattern issues with `Nothing` class
- Addressed code duplication in `Ok`/`Err` implementations
- Fixed inconsistent empty line formatting
- Implemented proper error type inheritance
- Fixed `TypeVar` pollution by using private TypeVars
- Improved error messaging in `do_notation`
- Added `__slots__` to reduce memory footprint
- Added missing docstrings to public API
- Fixed `Err.__hash__` to avoid mutable default issues
- Implemented proper `copy` and `deepcopy` support

### Removed
- Removed duplicate code in `Ok`/`Err` implementations

## [1.0.0] - 2026-02-10

### Added
- Initial release of RustyMonad
- `Option` type with `Some` and `Nothing` variants
- `Result` type with `Ok` and `Err` variants
- Monadic operations: `map`, `flatmap`, `and_then`, `or_else`
- Do-notation decorator for linear monadic code
- Try-decorator for automatic Result conversion
- Pattern matching support with Python 3.10+ match-case
- Error handling with custom exceptions
- Error mapping and transformation utilities
- Operator overloading for `>>` chaining

[Unreleased]: https://github.com/AkiSun/rustymonad/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/AkiSun/rustymonad/releases/tag/v1.0.0
