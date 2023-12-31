import {Color} from "@/models";

export function parseRGB(rgbString: string): Color {
    const match = rgbString.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    if (match) {
        return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
    }
    return [255, 255, 255]; // Default value if the string doesn't match the expected format
}

export function colorTupleToRGBString(color: Color): string {
    return `rgb(${color[0]},${color[1]},${color[2]})`;
}


export function camelCaseToWords(input: string): string {
    // Regular expression to match camel case pattern
    const camelCaseRegex = /([a-z])([A-Z])/g;

    // Replace camel case with space and capitalize
    const result = input.replace(camelCaseRegex, "$1 $2").replace(/\b\w/g, c => c.toUpperCase());

    return result;
}



export function toReadableString(input: string) {
    if (typeof input !== 'string') {
        return input;
    }

    return input
        .replace(/_/g, ' ')
        .replace(/-/g, ' ')
        .replace(/([a-z])([A-Z])/g, '$1 $2')
        .toLowerCase()
        .replace(/\b\w/g, char => char.toUpperCase());
}

// export function toLower
