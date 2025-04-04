import React, { memo, type ReactNode } from 'react';

import { Handle, Position, type Node, type NodeProps } from '@xyflow/react';

export type TurboNodeData = {
  title: string;
  icon?: ReactNode;
  topIcon?: ReactNode;
  subline?: string;
};

export default memo(({ data }: NodeProps<Node<TurboNodeData>>) => {
  return (
    <>
      <div className="cloud gradient">
        <div>
          {data.topIcon}
        </div>
      </div>
      <div className="wrapper gradient">
        <div className="inner">
          <div className="body">
            {data.icon && <div className="icon">{data.icon}</div>}
            <div>
              <div className="title">{data.title}</div>
              {data.subline && <div className="subline">{data.subline}</div>}
            </div>
          </div>
          <Handle type="target" position={Position.Left} />
          <Handle type="source" position={Position.Right} />
        </div>
      </div>
    </>
  );
});
