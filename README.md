# Convert STM's CubeMX generated register macro to Rust code

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
