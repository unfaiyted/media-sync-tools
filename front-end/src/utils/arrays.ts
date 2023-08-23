import {Color} from "@/models";
import {parseRGB} from "@/utils/string";

export function validateColors(colors: Color[] | undefined): Color[] {
    if(!colors) {
        return [];
    }

    return colors.map(color => {
        if (typeof color === 'string') {
            return parseRGB(color);
        }
        return color;
    });
}
