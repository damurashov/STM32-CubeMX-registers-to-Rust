# Convert STM's CubeMX generated register macros to Rust code

Heuristic ad-hoc code translator. Parses register values from CubeMX-generated C-files, filters out missing identifiers, and converts parsed values into valid Rust code. As a result, you will get something like:

```Rust
const USART1_BASE: u32 = (APBPERIPH_BASE + 0x00013800u32);
const TIM16_BASE: u32 = (APBPERIPH_BASE + 0x00014400u32);
const TIM17_BASE: u32 = (APBPERIPH_BASE + 0x00014800u32);
const DBGMCU_BASE: u32 = (APBPERIPH_BASE + 0x00015800u32);
const DMA1_BASE: u32 = (AHBPERIPH_BASE + 0x00000000u32);
const DMA1_Channel1_BASE: u32 = (DMA1_BASE + 0x00000008u32);
const DMA1_Channel2_BASE: u32 = (DMA1_BASE + 0x0000001Cu32);
const DMA1_Channel3_BASE: u32 = (DMA1_BASE + 0x00000030u32);
const DMA1_Channel4_BASE: u32 = (DMA1_BASE + 0x00000044u32);
```

In essence, the approach decomposes into 2 stages:

Stage 1 - parse define constants

1. Parse preprocessor definitions which follow key-value structure
2. Filter out preprocessor definitions which reference some identifiers that are not present in the file
3. Translate those k-v defines into Rust code

Stage 2 - parse register offsets

1. Unlike the the previous ones, register offsets are mapped onto memory through use of C structs. So the parser matches the structs that follow `typedef struct {...} *_TypeDef` pattern, parse the body of the structure, calculate offsets based on the type of the structure's member, and translate that into Rust code. On the offset calculation stage, type of the struct's member **is taken into account**, so a member defined as `uint16_t` will not erroneously advance the accumulated offset by `0x4`.
