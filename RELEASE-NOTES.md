# Release Notes

## `v0.1`
- Early pre-release
- Create a `bibliography.bib` file in the working directory or read one if it exists.
- Generate `bibtex` citation for any paper by DOI (e.g., `10.1371/journal.pone.0173664`)
- Add or remove citation from `bibliography.bib`.
- Manage conflicting biliography keys.
- View all citations within `bibliography.bib`.

## `v0.2`
- Create a `citeman.p` file in the working directory or read it if it exists. This `pickle` file retains query history between iterations of the program.
- Can now view query history.
- When viewing a citation in "Show Citations", now displays the citation with most recent updates to fields or key.
- General UI improvements.
- Codebase refactoring to improve readability
- Started to add very basic testing.