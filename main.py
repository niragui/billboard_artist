from src.archive_checker import ArchiveChecker


checker = ArchiveChecker()

website = checker.check_artist("Taylor Swift", "Billboard 200")

print(len(website.entries))
print(website.create_json())
