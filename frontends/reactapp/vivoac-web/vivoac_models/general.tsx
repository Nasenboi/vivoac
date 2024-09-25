export interface Address {
    street?: string;
    city?: string;
    state?: string;
    country?: string;
    postal_code?: string;
}

export interface AudioFormat {
    codec?: "aac" | "mp3" | "ogg" | "wav";
    sample_rate?: number;
    channels?: number;
    bit_depth?: number;
    bit_rate?: number;
    normalization_type?: "None" | "Peak" | "Loudness";
}

export interface LoginForm {
    username: string;
    password: string;
}