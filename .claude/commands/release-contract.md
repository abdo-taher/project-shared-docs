---
description: Listen for pushes to the Capitalix backend and run the whole contract release cycle; relay approval links
---

Run the release listener in the background and keep it running:

```
python3 tools/publish/capitalix_release.py --watch $ARGUMENTS
```

Use Bash with `run_in_background`. Do not stop it. Whenever its output prints `ACTION NEEDED`, tell the user at once,
with the exact link on the next line, and say what to click:

- a run link: open it, click "Review deployments", tick `contract-publisher`, "Approve and deploy";
- a pull request link: review the files, approve and merge it.

Never approve, merge or publish yourself. If the output says `STOPPED` or `REFUSED`, report the reason verbatim and keep
listening. Do not pass `--allow-breaking` or `--allow-unknown` unless the user explicitly asks for it in this message.
