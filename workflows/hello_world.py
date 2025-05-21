from flytekit import task, workflow

@task
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

@workflow
def hello_wf(name: str = "World") -> str:
    return say_hello(name=name)

if __name__ == "__main__":
    result = hello_wf(name="World")
    print(result) 