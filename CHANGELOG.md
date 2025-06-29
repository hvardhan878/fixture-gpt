# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-20

### Added
- Initial release of FixtureGPT
- Core `snapshot()` function for recording and replaying expensive function calls
- Support for environment variable control (`FIXTUREGPT_MODE=record|replay`)
- JSON fixture storage with SHA256 hashing for deduplication
- CLI interface with `stats`, `diff`, and `clear` commands
- Rich terminal output with cost estimation
- Graceful handling of non-JSON-serializable objects
- Support for LLM calls, tool outputs, and RAG pipeline results
- Comprehensive documentation and examples

### Features
- Record mode: Execute functions and save results to `./fixtures/`
- Replay mode: Return cached results without executing functions
- Automatic fixture deduplication using input hashing
- Cost estimation for LLM calls ($0.002 per call default)
- Beautiful CLI with Rich formatting
- Fallback to live execution when fixtures don't exist

### Dependencies
- typer>=0.9.0
- rich>=13.0.0
- Python>=3.8 