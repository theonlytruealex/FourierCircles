function coef = get_coef(points, n)
  coef = [0, 0];
  
  N = length(points(1,:)) - 1;
  if mod(N, 2) ~= 0
    error('Number of intervals must be even, so the number of points must be odd.');
  end

  h = 1 / N;

  sum1 = 0;
  sum2 = 0;
  % we use Simpson integration to calculate each coefficient
  for j = 2:N
    img_point = (points(1, j) + i * points(2, j)) * exp(-n * 2 * pi * i * (j - 1) * h);
    if mod(j, 2) == 0
      sum1 = sum1 + img_point;
    else
      sum2 = sum2 + img_point;
    end
  end
  coef(1) = (h / 3) * (points(1,1) + 4 * real(sum1) + 2 * real(sum2) + points(1,end));
  coef(2) = (h / 3) * (points(2,1) + 4 * imag(sum1) + 2 * imag(sum2) + points(2,end));
end