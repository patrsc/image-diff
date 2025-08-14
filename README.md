# image-diff

Install dependencies:

```
poetry install
npm install
```

## Usage

1. Hash images (create file `hashes.json`):

    ```
    poetry run python image-hash.py <FOLDER>
    ```

2. Make `clusters.json` file, run (threshold = `10`):

    ````
    poetry run python image-cluster.py 10
    ````

3. Start GUI to visualize similar image clusters from `clusters.json` file:

    ````
    npm start
    ````
