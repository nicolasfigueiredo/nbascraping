clear;

data = csvread('final_data_2xm_14_15.csv', 1, 1);
data2 = csvread('final_data_2xm_13_14.csv',1,1);
data3 = csvread('final_data_2xm_12_13.csv',1,1);

all_data = [data;data2;data3];
data = all_data(1:2300,:);

% 1-4: away off stats
% 5-8: away def stats
% 9: away pace
% 10-13: home off stats
% 14-17: home def stats
% 18: home pace
% 19: away pts
% 20: home pts

home_pace = repmat(data(:, 22), 1, 8);
away_pace = repmat(data(:, 11), 1, 8);

home_pts_data = horzcat(data(:,5:8), data(:,12:15));
away_pts_data = horzcat(data(:,1:4), data(:,16:19));

home_pts_data = horzcat(home_pts_data.*home_pace, home_pts_data.*away_pace, home_pts_data);
away_pts_data = horzcat(away_pts_data.*home_pace, away_pts_data.*away_pace, away_pts_data);

final_data_home = horzcat(home_pts_data, data(:,24));
final_data_away = horzcat(away_pts_data, data(:,23));

X_home = final_data_home(:, 1:24);
X_away = final_data_away(:, 1:24);
y_home = final_data_home(:,25);
y_away = final_data_away(:,25);
m = length(y_home);

% Scale features and set them to zero mean
fprintf('Normalizing Features ...\n');

[X_home mu sigma] = featureNormalize(X_home);
[X_away mu sigma] = featureNormalize(X_away);

% Add intercept term to X
X_home = [ones(m, 1) X_home];
X_away = [ones(m, 1) X_away];

fprintf('Running gradient descent ...\n');

% Choose some alpha value
alpha = 0.3;

num_iters = 200;

% Init Theta and Run Gradient Descent 
theta_home = zeros(25, 1);
theta_away = zeros(25, 1);
[theta_home, J_history] = gradientDescentMulti(X_home, y_home, theta_home, alpha, num_iters);
[theta_away, J_history] = gradientDescentMulti(X_away, y_away, theta_away, alpha, num_iters);

% Plot the convergence graph
figure;
plot(1:numel(J_history), J_history, '-b', 'LineWidth', 2);
xlabel('Number of iterations');
ylabel('Cost J');



%-------------TESTING-----------
data_t = all_data(2301:2880,:);

home_pace_t = repmat(data_t(:, 22), 1, 8);
away_pace_t = repmat(data_t(:, 11), 1, 8);

home_pts_data_t = horzcat(data_t(:,5:8), data_t(:,12:15));
away_pts_data_t = horzcat(data_t(:,1:4), data_t(:,16:19));

home_pts_data_t = horzcat(home_pts_data_t.*home_pace_t, home_pts_data_t.*away_pace_t, home_pts_data_t);
away_pts_data_t = horzcat(away_pts_data_t.*home_pace_t, away_pts_data_t.*away_pace_t, away_pts_data_t);

final_data_home_t = horzcat(home_pts_data_t, data_t(:,24));
final_data_away_t = horzcat(away_pts_data_t, data_t(:,23));

X_home_t = final_data_home_t(:, 1:24);
X_away_t = final_data_away_t(:, 1:24);
y_home_t = final_data_home_t(:,25);
y_away_t = final_data_away_t(:,25);
m = length(y_home_t);

[X_home_t mu sigma] = featureNormalize(X_home_t);
[X_away_t mu sigma] = featureNormalize(X_away_t);

% Add intercept term to X
X_home_t = [ones(m, 1) X_home_t];
X_away_t = [ones(m, 1) X_away_t];

h_y_home = X_home_t*theta_home;
h_y_away = X_away_t*theta_away;

result_home = abs(y_home_t-h_y_home);
result_away = abs(y_away_t-h_y_away);
result_total = abs(y_home_t+y_away_t-h_y_home-h_y_away);

fprintf('\nMean home pts: %.2f\nStd dev home pts: %.2f\n', mean(result_home), std(result_home));
fprintf('Mean away pts: %.2f\nStd dev away pts: %.2f\n', mean(result_away), std(result_away));
fprintf('Mean total pts: %.2f\nStd dev total pts: %.2f\n\n', mean(result_total), std(result_total));