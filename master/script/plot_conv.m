% plot_conv ('c1-8_c2-8_c3-8_c4-8_c5-8_fc6-8_fc7-64_seed1350')

function plot_conv(expname)

plot_path = sprintf( '%s/plots', getenv('COLOMBE_ROOT'));

% Plot matrix: NUM_TESTS x NUM_OUTS x K_WID x K_HGT
filename = sprintf('%s/%s.gif', plot_path, expname);

figure(1);

for layer = 1:8
    if (layer < 6)
        layer_id = 'conv';
    else
        layer_id = 'fc';
    end
    
    layer_str = sprintf( '%s/%s_%s%d.mat', plot_path, expname, layer_id, layer );

    load(layer_str);
    sz = size(weights)
    
    close(1)
    figure(1)
    set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
    
    NUM_TESTS   = sz(1);
    NUM_OUTS    = sz(2);
    
    if (layer == 1)
        NUM_INS     = 1;
        K_HGT       = sz(3);
        K_WID       = sz(4);
    else
        if (layer < 6)
            NUM_INS     = sz(3);
            K_HGT       = sz(4);
            K_WID       = sz(5);
        else
            NUM_INS     = sz(3);
            K_HGT       = 1;
            K_WID       = 1;
        end
    end
    
    sprintf( 'NUM_TESTS =%d\n', NUM_TESTS )            
    sprintf( 'NUM_OUTS  =%d\n', NUM_OUTS  )            
    sprintf( 'NUM_INS   =%d\n', NUM_INS   )            
    sprintf( 'K_HGT     =%d\n', K_HGT     )            
    sprintf( 'K_WID     =%d\n', K_WID     )            

    wid = 0.9/K_WID;
    hgt = 0.9/K_HGT;
    
    for the_out = 1:NUM_OUTS
        if (K_HGT > 1)

            % Convolutional layer
            for idx_v = 1:K_HGT
                for idx_h = 1:K_WID
                    plot_idx = (idx_v-1)*K_WID + idx_h;
                    if (NUM_INS > 1)
                        the_im = squeeze(weights( :, the_out, :, idx_v, idx_h));   % plot produces one trace per column
                        sz = size(the_im);
                        % sprintf( 'size(the_im)=%d %d', sz(1), sz(2) )
                    else
                        the_im = squeeze(weights( :, the_out, idx_v, idx_h));
                    end
        %            subplot( 11, 11, the_out ); imshow( the_im,[min(the_im(:)), max(the_im(:))] );
                    lft = (idx_h-1+0.05)/K_WID;
                    bot = (K_HGT-idx_v+0.05)/K_HGT;
                    p = [lft bot wid hgt];
                    h = subplot( 'Position', p );
                    %set(h, 'pos', p);
                    
                    plot(the_im); axis( [0 100 -0.2 0.2] );set(gca,'xticklabel',[]);set(gca,'yticklabel',[]);
                    set(gca,'XTick',0:20:100);
                    set(gca,'YTick',-0.2:0.1:0.2);
                    grid on
                end     % idx_h
            end         % idx_v
        else
            % K_HGT = 1
            
            % Fully-connected layer
            NUM_VER = ceil(sqrt(NUM_INS));
            NUM_HOR = ceil(sqrt(NUM_INS));
            wid = 0.9/NUM_HOR;
            hgt = 0.9/NUM_VER;
    
            for idx_v = 1:NUM_VER
                for idx_h = 1:NUM_HOR
                    plot_idx = (idx_v-1)*NUM_HOR + idx_h;
                    if (plot_idx <= NUM_INS)
                        % TEST, OUTPUT, INPUT
                        the_im = squeeze(weights( :, the_out, plot_idx));
                        lft = (idx_h-1+0.05)/NUM_HOR;
                        bot = (NUM_VER-idx_v+0.05)/NUM_VER;
                        p = [lft bot wid hgt];
                        h = subplot( 'Position', p );
                        %set(h, 'pos', p);
                        
                        plot(the_im); axis( [0 100 -0.2 0.2] );set(gca,'xticklabel',[]);set(gca,'yticklabel',[]);
                        set(gca,'XTick',0:20:100);
                        set(gca,'YTick',-0.2:0.1:0.2);
                        grid on
                    end
                end     % idx_h
            end         % idx_v
            
        end
        drawnow
    
        frame = getframe(1);
        im = frame2im(frame);
        [imind,cm] = rgb2ind(im,256);
        if (the_out == 1 && layer == 1)
          imwrite(imind,cm,filename,'gif', 'Loopcount',inf);
        else
          imwrite(imind,cm,filename,'gif','WriteMode','append');
        end
    end                 % the_out
                
end                     % layer
