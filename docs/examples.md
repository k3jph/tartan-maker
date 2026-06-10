# Example tartans

The `examples/` directory contains reference YAML files for published tartans. They are included so renderer behavior can be exercised against familiar symmetrical and asymmetrical setts.

## Included files

| File | Name | Sett type | SRT reference |
| --- | --- | --- | --- |
| `black-watch-government.yaml` | Black Watch / Government | symmetrical | 277 |
| `balmoral-original.yaml` | Balmoral (Original) | symmetrical | 182 |
| `rob-roy-macgregor.yaml` | Rob Roy MacGregor | symmetrical | 3516 |
| `buchanan.yaml` | Buchanan | asymmetrical | 414 |
| `royal-stewart.yaml` | Royal Stewart | symmetrical | 3958 |
| `macleod-of-lewis.yaml` | MacLeod of Lewis | symmetrical | 2630 |

## Why these examples?

- Black Watch is a compact, familiar symmetrical sett.
- Balmoral exercises gray-scale palette handling and explicit pivots.
- Rob Roy MacGregor is intentionally simple and large-scale.
- Buchanan is the important asymmetrical test case.
- Royal Stewart is a famous symmetrical tartan with a larger registered pallet than the supplied threadcount uses.
- MacLeod of Lewis provides a high-contrast yellow/red/black example.

## Rendering all examples

```bash
for spec in examples/*.yaml; do
  name=$(basename "$spec" .yaml)
  tartan-maker render "$spec" -o "$name.svg"
done
```

PNG output requires the optional `png` dependency:

```bash
pip install -e ".[png]"
```
