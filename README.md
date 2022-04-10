# Convert STM's CubeMX generated register values to Rust code

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
const DMA1_Channel5_BASE: u32 = (DMA1_BASE + 0x00000058u32);
const RCC_BASE: u32 = (AHBPERIPH_BASE + 0x00001000u32);
const FLASH_R_BASE: u32 = (AHBPERIPH_BASE + 0x00002000u32);
const OB_BASE: u32 = 0x1FFFF800u32;
const FLASHSIZE_BASE: u32 = 0x1FFFF7CCu32;
const UID_BASE: u32 = 0x1FFFF7ACu32;
const CRC_BASE: u32 = (AHBPERIPH_BASE + 0x00003000u32);
const GPIOA_BASE: u32 = (AHB2PERIPH_BASE + 0x00000000u32);
const GPIOB_BASE: u32 = (AHB2PERIPH_BASE + 0x00000400u32);
```
