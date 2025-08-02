import React from 'react';
import { SajuFormData } from '../../services/sajuApi';
import {
  Form,
  FormGroup,
  Label,
  Input,
  Select,
  Button
} from './styles/SharedStyles';

interface SajuFormProps {
  formData: SajuFormData;
  loading: boolean;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
}

const SajuForm: React.FC<SajuFormProps> = ({
  formData,
  loading,
  onInputChange,
  onSubmit
}) => {
  return (
    <Form onSubmit={onSubmit}>
      <FormGroup>
        <Label>이름</Label>
        <Input
          type="text"
          name="name"
          value={formData.name}
          onChange={onInputChange}
          placeholder="이름을 입력하세요"
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>생년월일</Label>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr 1fr",
            gap: "10px",
          }}
        >
          <Input
            type="number"
            name="year"
            value={formData.year}
            onChange={onInputChange}
            placeholder="년 (예: 1990)"
            min="1900"
            max="2100"
            required
          />
          <Input
            type="number"
            name="month"
            value={formData.month}
            onChange={onInputChange}
            placeholder="월 (1-12)"
            min="1"
            max="12"
            required
          />
          <Input
            type="number"
            name="day"
            value={formData.day}
            onChange={onInputChange}
            placeholder="일 (1-31)"
            min="1"
            max="31"
            required
          />
        </div>
      </FormGroup>

      <FormGroup>
        <Label>태어난 시간</Label>
        <Select
          name="hour"
          value={formData.hour}
          onChange={onInputChange}
          required
        >
          <option value="">시간을 선택하세요</option>
          {Array.from({ length: 24 }, (_, i) => (
            <option key={i} value={i}>
              {i}시
            </option>
          ))}
        </Select>
      </FormGroup>

      <FormGroup>
        <Label>성별</Label>
        <Select
          name="gender"
          value={formData.gender}
          onChange={onInputChange}
        >
          <option value="male">남성</option>
          <option value="female">여성</option>
        </Select>
      </FormGroup>

      <Button type="submit" disabled={loading}>
        {loading ? "종합 분석 중... (사주 + 대운 + 세운 + 연애운)" : "🔮 종합 사주 분석하기 (사주 + 대운 + 세운 + 연애운)"}
      </Button>
    </Form>
  );
};

export default SajuForm;