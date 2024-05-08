from metapython import *

importLib("asyncio")

print(asyncio)
importLib("uvloop")


def current_event_loop_exists() -> bool:
  try:
    asyncio.get_running_loop()
    return True
  except RuntimeError:
    return False


async def main():
  print("Main async loop running")


if (not current_event_loop_exists()):
  if sys.version_info >= (3, 11):
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
      runner.run(main())
  else:
    uvloop.install()
    asyncio.run(main())
else:
  asyncio.create_task(main())


# Async utility functions
async def astart():
  await asyncio.sleep(0)


async def go(task):
  await asyncio.sleep(0)
  return task


# Improved promise function using xargs and xapply
async def promise(task_func, fargs):
  task = asyncio.create_task(xapply(task_func, fargs))
  await astart()  # Ensure the task is scheduled
  task.start = astart  # Provide a way to manually yield control
  task.resolved = False  # Track resolution status
  return task
