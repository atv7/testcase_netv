import asyncio
import random
import string
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


async def generate_random_string(length=16):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


@app.post("/insert_random_entries")
async def insert_random_entries():
    base_url = "http://host.docker.internal:8000"

    num_entries = random.randint(10, 100)

    async with httpx.AsyncClient() as client:
        for _ in range(num_entries):
            text = await generate_random_string()
            response = await client.post(f"{base_url}/uuid/new", json={"text": text})
            if response.status_code == 200:
                print(f"Inserted entry: {text}")
            else:
                raise HTTPException(
                    status_code=500, detail=f"Failed to insert entry: {text}")

    print(f"Inserted {num_entries} random entries.")
    return {"message": f"Inserted {num_entries} random entries."}


@app.delete("/delete_entries")
async def delete_entries():
    base_url = "http://host.docker.internal:8000"
    batch_size = 10

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(f"{base_url}/uuid/count/{batch_size}")
            entries = response.json()
            if entries == {'detail': 'Not Found'}:
                break
            for entry in entries:
                await client.delete(f"{base_url}/uuid/{entry['uuid']}")
            print(f"Deleted {len(entries)} entries")

            await asyncio.sleep(10)

    print("Deletion process completed.")
    return {"message": "Deletion process completed."}
