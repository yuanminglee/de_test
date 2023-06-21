from prefect.filesystems import GitHub

gh_block = GitHub(
    name="etl", repository="https://github.com/yuanminglee/de_test"
)

gh_block.save("etl", overwrite=True)
