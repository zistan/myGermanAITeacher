export interface ApiError {
  detail: string;
  status_code?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export type DifficultyLevel = 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';

export type MasteryLevel = 0 | 1 | 2 | 3 | 4 | 5;

export interface DateRange {
  start_date: string;
  end_date: string;
}
