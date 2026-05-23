#include "../brush.hpp"

namespace picovector {


  void direct16_brush_span_func(image_t *target, brush_t *brush, int x, int y, int w) {
    direct16_brush_t *p = (direct16_brush_t*)brush;
    uint32_t *dst = (uint32_t*)target->ptrT(x, y);
    uint16_t src16 = p->c;

    // Alpha blending in RGB565 is possible but slow
    if(target->alpha() != 255) {
      // src16 = blend565(...);
    }
    uint32_t src = src16 << 16 | src16;

    // Would need separate blend functions?
    // blend_func_t fn = target->_blend_func;
    if (w & 1)
    {
        uint16_t* dst16 = (uint16_t*)dst;
        *dst16++ = src16;
        dst = (uint32_t*)dst16;
        w--;
    }
    while(w > 0) {
      *dst++ = src;
      w -= 2;
    }
  }

  void direct16_brush_masked_span_func(image_t *target, brush_t *brush, int x, int y, int w, uint8_t *mask) {
    direct16_brush_t *p = (direct16_brush_t*)brush;
    uint16_t *dst16 = (uint16_t*)target->ptrT(x, y);
    uint16_t src16 = p->c;

    // Alpha blending in RGB565 is possible but slow
    if(target->alpha() != 255) {
      // src16 = blend565(...);
    }

    // TODO: combine writes like the above function
    while (w>0) {
        if (*mask++ == 255) {
            *dst16++ = src16;
        } else {
            dst16++;
        }
        w--;
    }
  }

  direct16_brush_t::direct16_brush_t(const color_t& src)  {
    c = (((src._p & 0xf8) << 8) | ((src._p & 0xfc00) >> 5) | ((src._p & 0xf80000) >> 19));
  }

  direct16_brush_t::direct16_brush_t(const uint16_t c) : c(c)  {
  }

  span_func_t direct16_brush_t::span_func() {
    return direct16_brush_span_func;
  }

  masked_span_func_t direct16_brush_t::masked_span_func() {
    return direct16_brush_masked_span_func;
  }

}
